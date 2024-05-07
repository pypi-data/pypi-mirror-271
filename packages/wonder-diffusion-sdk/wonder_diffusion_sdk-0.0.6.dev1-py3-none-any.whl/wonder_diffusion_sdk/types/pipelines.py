from .pipeline_type import WonderPipelineType

from diffusers import (
    StableDiffusionPipeline,
    StableDiffusionImg2ImgPipeline,
    StableDiffusionInpaintPipeline,
    StableDiffusionControlNetPipeline,
    StableDiffusionControlNetImg2ImgPipeline,
    StableDiffusionXLPipeline,
    StableDiffusionXLImg2ImgPipeline,
    StableDiffusionXLInpaintPipeline,
    StableDiffusionXLControlNetPipeline,
    StableDiffusionXLControlNetImg2ImgPipeline)

PIPELINE_MAP = {
    WonderPipelineType.STABLE_DIFFUSION: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_IMG2IMG: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_img2img_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_INPAINT: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_inpaint_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_CONTROLNET: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_controlnet_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_CONTROLNET_IMG2IMG: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_controlnet_img2img_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_XL: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_xl_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_XL_IMG2IMG: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_xl_img2img_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_XL_INPAINT: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_xl_inpaint_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_XL_CONTROLNET: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_xl_controlnet_pipeline(pretrained_model_name_or_path, **kwargs),
    WonderPipelineType.STABLE_DIFFUSION_XL_CONTROLNET_IMG2IMG: lambda pretrained_model_name_or_path, **kwargs: initialize_stable_diffusion_xl_controlnet_img2img_pipeline(pretrained_model_name_or_path, **kwargs),
}


def initialize_stable_diffusion_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_img2img_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionImg2ImgPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_controlnet_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionControlNetPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_controlnet_img2img_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionControlNetImg2ImgPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_inpaint_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionInpaintPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_xl_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionXLPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_xl_img2img_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionXLImg2ImgPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_xl_inpaint_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionXLInpaintPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_xl_controlnet_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionXLControlNetPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_stable_diffusion_xl_controlnet_img2img_pipeline(pretrained_model_name_or_path, **kwargs):
    return StableDiffusionXLControlNetImg2ImgPipeline.from_pretrained(pretrained_model_name_or_path, **kwargs)
