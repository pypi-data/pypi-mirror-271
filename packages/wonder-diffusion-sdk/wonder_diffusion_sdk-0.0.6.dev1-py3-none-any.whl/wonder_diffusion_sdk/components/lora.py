import copy
import torch
import logging

from diffusers import (
    DiffusionPipeline,
    UNet2DConditionModel
)

from ..config import WonderLoraConfig, DEVICE


def load_loras_with_peft(pipeline: DiffusionPipeline, config: WonderLoraConfig, logger: logging.Logger):
    try:
        from peft import get_peft_model, PeftModel
    except Exception as e:
        logger.error(
            f'Failed to import peft: {e}')
        return

    peft_models = []
    adapters = []
    adapter_weights = []
    for lora in config.loras:
        # Load the lora's base unet model
        unet = UNet2DConditionModel.from_pretrained(
            lora.base_model_name_or_path,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
            subfolder="unet",
        ).to(DEVICE)

        # Load a temporary pipeline to load the lora weights
        temp_pipeline = DiffusionPipeline.from_pretrained(
            lora.base_model_name_or_path,
            torch_dtype=torch.float16,
            variant="fp16",
            unet=unet
        ).to(DEVICE)

        temp_pipeline.load_lora_weights(
            lora.path, weight_name=lora.weight_name, adapter_name=lora.adapter_name)
        temp_pipeline.set_adapters(adapter_names=lora.adapter_name)

        adapters.append(lora.adapter_name)
        adapter_weights.append(lora.adapter_weight)

        unet_copy = copy.deepcopy(unet)
        peft_model = get_peft_model(
            unet_copy,
            temp_pipeline.unet.peft_config[lora.adapter_name],
            adapter_name=lora.adapter_name
        )

        original_state_dict = {f"base_model.model.{k}": v for k,
                               v in temp_pipeline.unet.state_dict().items()}
        peft_model.load_state_dict(original_state_dict, strict=True)
        peft_model.save_pretrained(f'peft_models/{lora.adapter_name}')

        peft_models.append(peft_model)

        del unet, unet_copy, temp_pipeline, peft_model
        torch.cuda.empty_cache()

    model = PeftModel.from_pretrained(
        pipeline.unet, f'peft_models/{adapters[0]}', adapter_name=adapters[0], subfolder=adapters[0], use_safetensors=True)
    for i in range(1, len(adapters)):
        model.load_adapter(
            f'peft_models/{adapters[i]}', adapter_name=adapters[i], subfolder=adapters[i], use_safetensors=True)

    combined_adapter = adapters[0]
    for i in range(1, len(adapters)):
        combined_adapter += f'_{adapters[i]}'

    model.add_weighted_adapter(
        adapters=adapters,
        weights=adapter_weights,
        adapter_name=combined_adapter,
        combination_type=config.peft_combination_type,
        density=config.peft_density
    )
    model.set_adapters(combined_adapter)

    pipeline.unet = model
