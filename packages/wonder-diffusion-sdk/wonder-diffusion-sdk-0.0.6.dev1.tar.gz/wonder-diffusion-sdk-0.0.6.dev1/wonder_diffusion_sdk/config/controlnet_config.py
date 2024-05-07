import os
from ..types.controlnet_type import WonderControlNetType


class WonderControlNet:
    def __init__(
        self,
        controlnet_type: WonderControlNetType | str,
        pretrained_model_name_or_path: str | os.PathLike = 'controlnet_models/',
        **kwargs
    ):
        self.controlnet_type = controlnet_type if type(
            controlnet_type) == WonderControlNetType else WonderControlNetType(controlnet_type)

        self.pretrained_model_name_or_path = pretrained_model_name_or_path

        self.kwargs = kwargs


class WonderControlNetConfig:
    """
    ControlNet model initialization wrapper.
    """

    def __init__(self, controlnets: list[WonderControlNet] = []):
        self.controlnets = controlnets
