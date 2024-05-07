import torch
import logging

from diffusers import (
    DiffusionPipeline,
    AutoencoderKL,
    UNet2DConditionModel
)


def get_precision_args(precision):
    args = {}
    if precision == 'bfloat16':
        args['torch_dtype'] = torch.bfloat16
    elif precision == 'float16':
        args['torch_dtype'] = torch.float16
        args['variant'] = 'fp16'
        args['use_safetensors'] = True
    return args


def half_precision_vae(pipeline: DiffusionPipeline, precision: str, DEVICE: str, logger: logging.Logger):
    logger.info('DIFFUSION SDK LOG: Using half precision VAE')
    dtype = torch.bfloat16 if precision == 'bfloat16' else torch.float16
    try:
        pipeline.vae = AutoencoderKL.from_pretrained(
            'madebyollin/sdxl-vae-fp16-fix', torch_dtype=dtype).to(DEVICE)
    except Exception as e:
        logger.error(
            f'Failed to load half precision VAE model: {e}')


def fuse_qkv_projections(pipeline: DiffusionPipeline, logger: logging.Logger):
    logger.info('DIFFUSION SDK LOG: Fusing QKV projections')
    try:
        pipeline.unet.fuse_qkv_projections()
        pipeline.vae.fuse_qkv_projections()
    except Exception as e:
        logger.error(
            f'Failed to fuse QKV projections: {e}')


def use_channels_last(pipeline: DiffusionPipeline, logger: logging.Logger):
    logger.info('DIFFUSION SDK LOG: Using channels last')
    try:
        pipeline.unet.to(memory_format=torch.channels_last)
    except Exception as e:
        logger.error(
            f'Failed to use channels last: {e}')
