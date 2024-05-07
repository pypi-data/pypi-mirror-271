from .controlnet_type import WonderControlNetType

from diffusers import ControlNetModel

CONTROLNET_MAP = {
    WonderControlNetType.DEPTH: lambda pretrained_model_name_or_path, **kwargs: initialize_depth_controlnet(pretrained_model_name_or_path, **kwargs),
    WonderControlNetType.CANNY: lambda pretrained_model_name_or_path, **kwargs: initialize_canny_controlnet(pretrained_model_name_or_path, **kwargs),
    WonderControlNetType.QR: lambda pretrained_model_name_or_path, **kwargs: initialize_qr_controlnet(pretrained_model_name_or_path, **kwargs),
}


def initialize_depth_controlnet(pretrained_model_name_or_path, **kwargs):
    return ControlNetModel.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_canny_controlnet(pretrained_model_name_or_path, **kwargs):
    return ControlNetModel.from_pretrained(pretrained_model_name_or_path, **kwargs)


def initialize_qr_controlnet(pretrained_model_name_or_path, **kwargs):
    return ControlNetModel.from_pretrained(pretrained_model_name_or_path, **kwargs)
