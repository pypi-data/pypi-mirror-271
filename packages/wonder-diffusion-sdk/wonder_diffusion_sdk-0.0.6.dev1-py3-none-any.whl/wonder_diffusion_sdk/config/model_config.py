import os

from .lora_config import WonderLoraConfig
from .controlnet_config import WonderControlNetConfig
from ..types.pipeline_type import WonderPipelineType
from ..types.scheduler_type import WonderSchedulerType

class WonderDiffusionModelConfig:

    def __init__(
        self,
        pipeline_type: WonderPipelineType | str,
        pretrained_model_name_or_path: str | os.PathLike = 'models/',
        initial_scheduler: WonderSchedulerType | str = WonderSchedulerType.DPM_SOLVER_MULTISTEP,
        precision: str = 'float16',
        lora_config: WonderLoraConfig = None,
        controlnet_config: WonderControlNetConfig = None,
        # Optimization variables
        use_half_precision_vae: bool = False,
        fuse_qkv_projections: bool = False,
        use_channels_last: bool = False,
        use_deep_cache: bool = False,
        # Lightning model variables
        use_lightning_model: bool = False,
        lightning_model_step_count: int = 4,

        **kwargs,
    ):
        self.pipeline_type = pipeline_type if type(
            pipeline_type) == WonderPipelineType else WonderPipelineType(pipeline_type)

        self.initial_scheduler = initial_scheduler if type(
            initial_scheduler) == WonderSchedulerType else WonderSchedulerType(initial_scheduler)

        self.pretrained_model_name_or_path = pretrained_model_name_or_path

        self.precision = precision
        self.use_half_precision_vae = use_half_precision_vae
        self.fuse_qkv_projections = fuse_qkv_projections
        self.use_channels_last = use_channels_last

        self.use_deep_cache = use_deep_cache

        self.use_lightning_model = use_lightning_model
        self.lightning_model_step_count = lightning_model_step_count

        self.lora_config = lora_config
        self.controlnet_config = controlnet_config

        self.kwargs = kwargs

        self.check_controlnet_pipeline_type()

    def check_controlnet_pipeline_type(self):
        if self.controlnet_config != None:
            assert self.pipeline_type.is_controlnet(), 'Pipeline type must be a controlnet pipeline type'
