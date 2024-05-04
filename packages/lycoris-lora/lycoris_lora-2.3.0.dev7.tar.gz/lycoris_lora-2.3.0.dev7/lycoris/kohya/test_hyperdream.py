# network module for kohya
# reference:
# https://github.com/microsoft/LoRA/blob/main/loralib/layers.py
# https://github.com/cloneofsimo/lora/blob/master/lora_diffusion/lora.py
# https://github.com/kohya-ss/sd-scripts/blob/main/networks/lora.py

import os
import re
import sys
from typing import List

sys.setrecursionlimit(10000)

import torch
import torch.utils.checkpoint as checkpoint

from .utils import *
from ..wrapper import LycorisNetwork
from ..modules.locon import LoConModule
from ..modules.loha import LohaModule
from ..modules.ia3 import IA3Module
from ..modules.lokr import LokrModule
from ..modules.dylora import DyLoraModule
from ..modules.glora import GLoRAModule
from ..modules.norms import NormModule
from ..modules.full import FullModule
from ..modules.diag_oft import DiagOFTModule
from ..modules.boft import ButterflyOFTModule
from ..modules import make_module

from ..config import PRESET
from ..utils.preset import read_preset
from ..utils import get_module, str_bool
from ..logging import logger


network_module_dict = {
    "lora": LoConModule,
    "locon": LoConModule,
    "loha": LohaModule,
    "ia3": IA3Module,
    "lokr": LokrModule,
    "dylora": DyLoraModule,
    "glora": GLoRAModule,
    "full": FullModule,
    "diag-oft": DiagOFTModule,
    "boft": ButterflyOFTModule,
}


def create_hypernetwork(
    multiplier,
    network_dim,
    network_alpha,
    vae,
    text_encoder,
    unet,
    vocab_size,
    **kwargs,
):
    if network_dim is None:
        network_dim = 4
    dropout = float(kwargs.get("dropout", 0.0) or 0.0)
    rank_dropout = float(kwargs.get("rank_dropout", 0.0) or 0.0)
    module_dropout = float(kwargs.get("module_dropout", 0.0) or 0.0)
    algo = (kwargs.get("algo", "lora") or "lora").lower()
    use_tucker = str_bool(
        not kwargs.get("disable_conv_cp", True)
        or kwargs.get("use_conv_cp", False)
        or kwargs.get("use_cp", False)
        or kwargs.get("use_tucker", False)
    )
    if "disable_conv_cp" in kwargs or "use_cp" in kwargs or "use_conv_cp" in kwargs:
        logger.warning(
            "disable_conv_cp and use_cp are deprecated. Please use use_tucker instead.",
            stacklevel=2,
        )
    block_size = int(kwargs.get("block_size", 4) or 4)
    down_dim = int(kwargs.get("down_dim", 128) or 128)
    up_dim = int(kwargs.get("up_dim", 64) or 64)
    delta_iters = int(kwargs.get("delta_iters", 5) or 5)
    decoder_blocks = int(kwargs.get("decoder_blocks", 4) or 4)
    network_module = {
        "lora": LoConModule,
        "locon": LoConModule,
    }[algo]

    logger.info(f"Using rank adaptation algo: {algo}")

    return HyperDreamNetwork(
        text_encoder,
        unet,
        multiplier=multiplier,
        lora_dim=network_dim,
        alpha=network_alpha,
        use_tucker=use_tucker,
        dropout=dropout,
        rank_dropout=rank_dropout,
        module_dropout=module_dropout,
        network_module=network_module,
        down_dim=down_dim,
        up_dim=up_dim,
        delta_iters=delta_iters,
        decoder_blocks=decoder_blocks,
        vocab_size=vocab_size,
        decompose_both=kwargs.get("decompose_both", False),
        factor=kwargs.get("factor", -1),
        block_size=block_size,
    )


class HyperDreamNetwork(torch.nn.Module):
    """
    HyperDreamBooth hypernetwork part
    only train Attention right now
    """

    UNET_TARGET_REPLACE_MODULE = [
        "Attention",
    ]
    UNET_TARGET_REPLACE_NAME = []
    TEXT_ENCODER_TARGET_REPLACE_MODULE = ["CLIPAttention"]
    LORA_PREFIX_UNET = "lora_unet"
    LORA_PREFIX_TEXT_ENCODER = "lora_te"

    def __init__(
        self,
        text_encoder,
        unet,
        multiplier=1.0,
        lora_dim=4,
        alpha=1,
        use_tucker=False,
        dropout=0,
        rank_dropout=0,
        module_dropout=0,
        network_module=LoConModule,
        down_dim=100,
        up_dim=50,
        delta_iters=5,
        decoder_blocks=4,
        vocab_size=49408,
        **kwargs,
    ) -> None:
        from ..modules.hypernet import ImgWeightGenerator, TextWeightGenerator

        super().__init__()
        self.gradient_ckpt = False
        self.multiplier = multiplier
        self.lora_dim = lora_dim
        self.alpha = alpha

        if 1 >= dropout >= 0:
            logger.info(f"Use Dropout value: {dropout}")
        if network_module != LoConModule:
            logger.info("HyperDreamBooth only support LoRA at this time")
            raise NotImplementedError
        if lora_dim * (down_dim + up_dim) > 4096:
            logger.info(
                "weight elements > 4096 (dim * (down_dim + up_dim)) is not recommended!"
            )

        self.dropout = dropout
        self.rank_dropout = rank_dropout
        self.module_dropout = module_dropout

        # create module instances
        def create_modules(
            prefix,
            root_module: torch.nn.Module,
            target_replace_modules,
            target_replace_names=[],
        ) -> List[network_module]:
            logger.info("Create LyCORIS Module")
            loras = []
            for name, module in root_module.named_modules():
                if module.__class__.__name__ in target_replace_modules:
                    for child_name, child_module in module.named_modules():
                        lora_name = prefix + "." + name + "." + child_name
                        lora_name = lora_name.replace(".", "_")
                        if child_module.__class__.__name__ == "Linear" and lora_dim > 0:
                            lora = network_module(
                                lora_name,
                                child_module,
                                self.multiplier,
                                self.lora_dim,
                                self.alpha,
                                self.dropout,
                                self.rank_dropout,
                                self.module_dropout,
                                use_tucker,
                                **kwargs,
                            )
                        elif child_module.__class__.__name__ == "Conv2d":
                            k_size, *_ = child_module.kernel_size
                            if k_size == 1 and lora_dim > 0:
                                lora = network_module(
                                    lora_name,
                                    child_module,
                                    self.multiplier,
                                    self.lora_dim,
                                    self.alpha,
                                    self.dropout,
                                    self.rank_dropout,
                                    self.module_dropout,
                                    use_tucker,
                                    **kwargs,
                                )
                            else:
                                continue
                        else:
                            continue
                        loras.append(lora)
                elif name in target_replace_names:
                    lora_name = prefix + "." + name
                    lora_name = lora_name.replace(".", "_")
                    if module.__class__.__name__ == "Linear" and lora_dim > 0:
                        lora = network_module(
                            lora_name,
                            module,
                            self.multiplier,
                            self.lora_dim,
                            self.alpha,
                            self.dropout,
                            self.rank_dropout,
                            self.module_dropout,
                            use_tucker,
                            **kwargs,
                        )
                    elif module.__class__.__name__ == "Conv2d":
                        k_size, *_ = module.kernel_size
                        if k_size == 1 and lora_dim > 0:
                            lora = network_module(
                                lora_name,
                                module,
                                self.multiplier,
                                self.lora_dim,
                                self.alpha,
                                self.dropout,
                                self.rank_dropout,
                                self.module_dropout,
                                use_tucker,
                                **kwargs,
                            )
                        else:
                            continue
                    else:
                        continue
                    loras.append(lora)
            return loras

        if isinstance(text_encoder, list):
            text_encoders = text_encoder
            use_index = True
        else:
            text_encoders = [text_encoder]
            use_index = False

        self.text_encoder_loras = []
        for i, te in enumerate(text_encoders):
            self.text_encoder_loras.extend(
                create_modules(
                    HyperDreamNetwork.LORA_PREFIX_TEXT_ENCODER
                    + (f"{i+1}" if use_index else ""),
                    te,
                    HyperDreamNetwork.TEXT_ENCODER_TARGET_REPLACE_MODULE,
                )
            )
        logger.info(
            f"create LyCORIS for Text Encoder: "
            f"{len(self.text_encoder_loras)} modules."
        )

        self.unet_loras = create_modules(
            HyperDreamNetwork.LORA_PREFIX_UNET,
            unet,
            HyperDreamNetwork.UNET_TARGET_REPLACE_MODULE,
        )
        logger.info(f"create LyCORIS for U-Net: {len(self.unet_loras)} modules.")

        self.loras: list[LoConModule] = self.text_encoder_loras + self.unet_loras
        self.img_weight_generater = ImgWeightGenerator(
            weight_dim=(down_dim + up_dim) * lora_dim,
            weight_num=len(self.unet_loras),
            sample_iters=delta_iters,
            decoder_blocks=decoder_blocks,
        )
        self.text_weight_generater = TextWeightGenerator(
            weight_dim=(down_dim + up_dim) * lora_dim,
            weight_num=len(self.text_encoder_loras),
            sample_iters=delta_iters,
            decoder_blocks=decoder_blocks,
        )
        self.split = (down_dim * lora_dim, up_dim * lora_dim)
        self.lora_dim = lora_dim

        self.weights_sd = None

        # assertion
        names = set()
        for lora in self.text_encoder_loras + self.unet_loras:
            assert (
                lora.lora_name not in names
            ), f"duplicated lora name: {lora.lora_name}"
            names.add(lora.lora_name)

        self.checkpoint = torch.nn.Parameter(torch.tensor(0.0))

        with torch.no_grad():
            self.update_reference(
                torch.randn(1, 3, *self.img_weight_generater.ref_size), ["test"]
            )

        # for lora in self.loras:
        #     assert torch.all(lora.data[0]==0)

    def gen_weight(self, ref_img, caption, iter=None, ensure_grad=0):
        unet_weights = self.img_weight_generater(ref_img, iter, ensure_grad=ensure_grad)
        unet_weights = unet_weights + self.checkpoint
        unet_weights = [
            i.split(self.split, dim=-1) for i in unet_weights.split(1, dim=1)
        ]
        text_weights = self.text_weight_generater(
            caption, iter, ensure_grad=ensure_grad
        )
        text_weights = text_weights + self.checkpoint
        text_weights = [
            i.split(self.split, dim=-1) for i in text_weights.split(1, dim=1)
        ]
        return unet_weights, text_weights

    def update_reference(self, ref_img, caption, iter=None):
        # use idx for aux weight seed
        if self.gradient_ckpt and self.training:
            ensure_grad = torch.zeros(1, device=ref_img.device, requires_grad=True)
            unet_weights_list, text_weights_list = checkpoint.checkpoint(
                self.gen_weight, ref_img, caption, iter, ensure_grad
            )
        else:
            unet_weights_list, text_weights_list = self.gen_weight(
                ref_img, caption, iter
            )

        for idx, (lora, weight) in enumerate(zip(self.unet_loras, unet_weights_list)):
            assert (
                lora.multiplier > 0
            ), f"multiplier must be positive: {lora.multiplier}"
            # weight: [batch, 1, weight_dim]
            # if weight.dim()==3:
            #     weight = weight.squeeze(1)
            lora.update_weights(*weight, idx)

        for idx, (lora, weight) in enumerate(
            zip(self.text_encoder_loras, text_weights_list)
        ):
            assert (
                lora.multiplier > 0
            ), f"multiplier must be positive: {lora.multiplier}"
            # weight: [batch, 1, weight_dim]
            # if weight.dim()==3:
            #     weight = weight.squeeze(1)
            lora.update_weights(*weight, idx)

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier
        for lora in self.text_encoder_loras + self.unet_loras:
            lora.multiplier = self.multiplier

    def load_weights(self, file):
        if os.path.splitext(file)[1] == ".safetensors":
            from safetensors.torch import load_file, safe_open

            self.weights_sd = load_file(file)
        else:
            self.weights_sd = torch.load(file, map_location="cpu")

    def apply_to(self, text_encoder, unet, apply_text_encoder=None, apply_unet=None):
        if self.weights_sd:
            weights_has_text_encoder = weights_has_unet = False
            for key in self.weights_sd.keys():
                if key.startswith(HyperDreamNetwork.LORA_PREFIX_TEXT_ENCODER):
                    weights_has_text_encoder = True
                elif key.startswith(HyperDreamNetwork.LORA_PREFIX_UNET):
                    weights_has_unet = True

            if apply_text_encoder is None:
                apply_text_encoder = weights_has_text_encoder
            else:
                assert (
                    apply_text_encoder == weights_has_text_encoder
                ), f"text encoder weights: {weights_has_text_encoder} but text encoder flag: {apply_text_encoder} / 重みとText Encoderのフラグが矛盾しています"

            if apply_unet is None:
                apply_unet = weights_has_unet
            else:
                assert (
                    apply_unet == weights_has_unet
                ), f"u-net weights: {weights_has_unet} but u-net flag: {apply_unet} / 重みとU-Netのフラグが矛盾しています"
        else:
            assert (
                apply_text_encoder is not None and apply_unet is not None
            ), f"internal error: flag not set"

        if apply_text_encoder:
            logger.info("enable LyCORIS for text encoder")
        else:
            self.text_encoder_loras = []

        if apply_unet:
            logger.info("enable LyCORIS for U-Net")
        else:
            self.unet_loras = []

        for lora in self.text_encoder_loras + self.unet_loras:
            lora.apply_to(is_hypernet=True)

    def enable_gradient_checkpointing(self):
        self.gradient_ckpt = True

    def prepare_optimizer_params(self, text_encoder_lr, unet_lr, learning_rate):
        self.requires_grad_(True)
        all_params = []

        if self.text_encoder_loras:
            all_params.append(
                {
                    "params": (
                        [
                            p
                            for p in self.text_weight_generater.decoder_model.parameters()
                        ]
                        + [
                            p
                            for p in self.text_weight_generater.pos_emb_proj.parameters()
                        ]
                        + [
                            p
                            for p in self.text_weight_generater.feature_proj.parameters()
                        ]
                        + (
                            [
                                p
                                for p in self.text_weight_generater.encoder_model.parameters()
                            ]
                            if self.text_weight_generater.train_encoder
                            else []
                        )
                    ),
                    "lr": text_encoder_lr,
                }
            )
        if self.unet_loras:
            all_params.append(
                {
                    "params": (
                        [
                            p
                            for p in self.img_weight_generater.decoder_model.parameters()
                        ]
                        + [
                            p
                            for p in self.img_weight_generater.pos_emb_proj.parameters()
                        ]
                        + [
                            p
                            for p in self.img_weight_generater.feature_proj.parameters()
                        ]
                        + (
                            [
                                p
                                for p in self.img_weight_generater.encoder_model.parameters()
                            ]
                            if self.img_weight_generater.train_encoder
                            else []
                        )
                    ),
                    "lr": unet_lr,
                }
            )
        return all_params

    def prepare_grad_etc(self, text_encoder, unet):
        self.requires_grad_(True)

    def on_epoch_start(self, text_encoder, unet):
        self.train()

    def get_trainable_params(self):
        return self.parameters()

    def save_weights(self, file, dtype, metadata):
        if metadata is not None and len(metadata) == 0:
            metadata = None

        state_dict = self.img_weight_generater.state_dict()
        if not self.img_weight_generater.train_encoder:
            for k in self.img_weight_generater.encoder_model.state_dict().keys():
                state_dict.pop(f"encoder_model.{k}")
        state_dict = {f"img_weight_generater.{i}": v for i, v in state_dict.items()}

        state_dict = self.text_weight_generater.state_dict()
        if not self.text_weight_generater.train_encoder:
            for k in self.text_weight_generater.encoder_model.state_dict().keys():
                state_dict.pop(f"encoder_model.{k}")
        state_dict = {f"text_weight_generater.{i}": v for i, v in state_dict.items()}

        if dtype is not None:
            for key in list(state_dict.keys()):
                v = state_dict[key]
                v = v.detach().clone().to("cpu").to(dtype)
                state_dict[key] = v

        if os.path.splitext(file)[1] == ".safetensors":
            from safetensors.torch import save_file

            # Precalculate model hashes to save time on indexing
            if metadata is None:
                metadata = {}
            model_hash, legacy_hash = precalculate_safetensors_hashes(
                state_dict, metadata
            )
            metadata["sshs_model_hash"] = model_hash
            metadata["sshs_legacy_hash"] = legacy_hash

            save_file(state_dict, file, metadata)
        else:
            torch.save(state_dict, file)
