import copy
import torch
import logging
from random import randint

from diffusers import DiffusionPipeline

from .types import (
    PIPELINE_MAP,
    SCHEDULER_MAP,
    CONTROLNET_MAP,
    WonderPipelineType,
    WonderSchedulerType,
    WonderControlNetType)

from .config import (
    DEVICE,
    WonderDiffusionSdkConfig,
    WonderDiffusionModelConfig,
    WonderLora,
    WonderLoraConfig,
    WonderControlNet,
    WonderControlNetConfig)

from .components import (
    setup_logger,
    get_precision_args,
    half_precision_vae,
    fuse_qkv_projections,
    use_channels_last,
)


class WonderDiffusionSdk:

    def __init__(self, config: WonderDiffusionSdkConfig, logger: logging.Logger = None):
        self.logger = logger if logger else setup_logger()

        self.logger.info(
            'DIFFUSION SDK LOG: Initializing Wonder Diffusion SDK')

        if config.enable_custom_safety_checker:
            self.initialize_safety_checker()

    def initialize_pipeline(self, model_config: WonderDiffusionModelConfig):
        # get precision related args
        args = get_precision_args(model_config.precision)
        model_config.kwargs.update(args)

        self.logger.info(
            f'DIFFUSION SDK LOG: Initializing pipeline with kwargs: {model_config.kwargs}')

        # initialize controlnets
        if model_config.controlnet_config != None:
            controlnets = []
            for c in model_config.controlnet_config.controlnets:
                controlnet = self.initialize_controlnet(c)
                controlnets.append(controlnet)
                controlnet.to(DEVICE)
            model_config.kwargs['controlnet'] = controlnets

        # initialize pipeline
        self.pipeline = PIPELINE_MAP[model_config.pipeline_type](
            model_config.pretrained_model_name_or_path, **model_config.kwargs)

        self.pipeline.scheduler = SCHEDULER_MAP[model_config.initial_scheduler](
            self.pipeline.scheduler.config)

        self.pipeline.to(DEVICE)

        # load loras
        if model_config.lora_config != None:
            self.initialize_loras(model_config.lora_config, self.pipeline)

        # apply optimizations based on model config
        if model_config.use_half_precision_vae:
            half_precision_vae(
                self.pipeline, model_config.precision, DEVICE, self.logger)

        if model_config.fuse_qkv_projections:
            fuse_qkv_projections(self.pipeline, self.logger)

        if model_config.use_channels_last:
            use_channels_last(self.pipeline, self.logger)

        # enable deep cache
        if model_config.use_deep_cache:
            self.enable_deepcache(self.pipeline)

        # enable lightning model
        if model_config.use_lightning_model:
            self.enable_lightning_model(
                self.pipeline, model_config.lightning_model_step_count)

        return self.pipeline

    # CONTROLNET
    def initialize_controlnet(self, controlnet: WonderControlNet):
        self.logger.info(
            f'DIFFUSION SDK LOG: Initializing controlnet with type: {controlnet.controlnet_type}')

        controlnet_model = CONTROLNET_MAP[controlnet.controlnet_type](
            controlnet.pretrained_model_name_or_path, **controlnet.kwargs)

        return controlnet_model

    # DEEPCACHE
    def enable_deepcache(self, pipeline: DiffusionPipeline):
        self.logger.info('DIFFUSION SDK LOG: Enabling deep cache')
        try:
            from .components import enable_deepcache
            self.deepcache_helper = enable_deepcache(pipeline)
        except Exception as e:
            self.logger.error(
                f'Failed to enable deep cache: {e}')

    def disable_deepcache(self):
        if hasattr(self, 'deepcache_helper'):
            self.logger.info('DIFFUSION SDK LOG: Disabling deep cache')
            self.deepcache_helper.disable()

    # LIGHTNING
    def enable_lightning_model(self, pipeline=None, step_count=4):
        curr_pipeline = None
        if pipeline != None:
            curr_pipeline = pipeline
        else:
            if hasattr(self, 'pipeline'):
                curr_pipeline = self.pipeline

        if curr_pipeline != None:
            self.logger.info('DIFFUSION SDK LOG: Enabling lightning model')
            try:
                from .components import enable_lightning
                enable_lightning(curr_pipeline, step_count)
            except Exception as e:
                self.logger.error(
                    f'Failed to enable lightning model: {e}')
            self.logger.info(
                f'DIFFUSION SDK LOG: Pipeline scheduler timestep_spacing: {curr_pipeline.scheduler.config.timestep_spacing}')
            self.logger.info(
                f'DIFFUSION SDK LOG: Pipeline scheduler prediction_type: {curr_pipeline.scheduler.config.prediction_type}')

    # Diffusion functions

    def set_scheduler(self, scheduler: WonderSchedulerType, pipeline: DiffusionPipeline = None):
        _pipeline = None
        if pipeline != None:
            _pipeline = pipeline
        elif hasattr(self, 'pipeline'):
            _pipeline = self.pipeline

        if _pipeline != None and scheduler in SCHEDULER_MAP:
            _pipeline.scheduler = SCHEDULER_MAP[scheduler](
                _pipeline.scheduler.config)

    def run(self, args: dict):
        args['generator'], seed = self.generate_seed(args.get('seed', None))
        self.logger.info(f'DIFFUSION SDK LOG: Seed {seed}')

        return self.pipeline(**args).images, seed

    def generate_seed(self, seed=None):
        if seed == None or seed < 0:
            seed = randint(0, 2**32-1)
        return torch.Generator(device=DEVICE).manual_seed(seed), seed

    # Safety checker

    def initialize_safety_checker(self):
        from transformers import AutoFeatureExtractor
        from .components import StableDiffusionSafetyChecker
        self.feature_extractor = AutoFeatureExtractor.from_pretrained(
            'CompVis/stable-diffusion-safety-checker')
        self.safety_checker = StableDiffusionSafetyChecker.from_pretrained(
            'CompVis/stable-diffusion-safety-checker').to(DEVICE)

    def safety_check(self, images):
        if not hasattr(self, 'safety_checker'):
            self.initialize_safety_checker()

        safety_checker_input = self.feature_extractor(
            images, return_tensors='pt').to(DEVICE)
        images, has_nsfw_concept = self.safety_checker(
            images=images, clip_input=safety_checker_input.pixel_values.to(torch.float16))
        return images, has_nsfw_concept

    # Lora

    def initialize_loras(self, config: WonderLoraConfig, pipeline: DiffusionPipeline = None):
        _pipeline = None
        if pipeline != None:
            _pipeline = pipeline
        elif hasattr(self, 'pipeline'):
            _pipeline = self.pipeline

        # Single Lora
        if len(config.loras) == 1:
            _pipeline.load_lora_weights(
                config.loras[0].path, weight_name=config.loras[0].weight_name)
        # Multiple Loras
        else:
            if config.use_peft:
                try:
                    from .components import load_loras_with_peft
                    load_loras_with_peft(_pipeline, config, self.logger)
                except Exception as e:
                    self.logger.error(
                        f'Failed to load Loras with peft: {e}')
            else:
                adapters = []
                adapter_weights = []
                for lora in config.loras:
                    _pipeline.load_lora_weights(
                        lora.path, weight_name=lora.weight_name, adapter_name=lora.adapter_name)
                    adapters.append(lora.adapter_name)
                    adapter_weights.append(lora.adapter_weight)
                _pipeline.set_adapters(
                    adapters, adapter_weights=adapter_weights)
