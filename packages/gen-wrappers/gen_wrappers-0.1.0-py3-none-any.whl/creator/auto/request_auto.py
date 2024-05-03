from dataclasses import field, dataclass
from typing import List, Dict, Any

from creator.base.base_request import BaseRequest


@dataclass
class AutoTxt2Img(BaseRequest):
    app = "AUTO"
    prompt: str = ""
    negative_prompt: str = ""
    styles: List[str] = field(default_factory=list)
    seed: int = -1
    subseed: int = -1
    subseed_strength: float = 0
    seed_resize_from_h: int = -1
    seed_resize_from_w: int = -1
    sampler_name: str = "Euler a"
    batch_size: int = 1
    n_iter: int = 1
    steps: int = 20
    cfg_scale: float = 7
    width: int = 1024
    height: int = 768
    restore_faces: bool = False
    tiling: bool = False
    do_not_save_samples: bool = True
    do_not_save_grid: bool = True
    eta: float = 0.0
    denoising_strength: float = 0.7
    s_min_uncond: float = 0.0
    s_churn: float = 0.0
    s_tmax: float = 0.0
    s_tmin: float = 0.0
    s_noise: float = 1.0
    override_settings: Dict[str, Any] = field(default_factory=dict)
    override_settings_restore_afterwards: bool = True
    refiner_checkpoint: str = ""  # Changed from None to ""
    refiner_switch_at: int = 0
    disable_extra_networks: bool = False
    firstpass_image: str = ""  # Changed from None to ""
    comments: Dict[str, Any] = field(default_factory=dict)
    enable_hr: bool = False
    firstphase_width: int = 0
    firstphase_height: int = 0
    hr_scale: int = 2
    hr_upscaler: str = "Latent"
    hr_second_pass_steps: int = 0
    hr_resize_x: int = 0
    hr_resize_y: int = 0
    hr_checkpoint_name: str = ""
    hr_sampler_name: str = ""
    hr_prompt: str = ""
    hr_negative_prompt: str = ""
    force_task_id: str = ""
    sampler_index: str = "0"
    script_name: str = ""
    script_args: List[Any] = field(default_factory=list)
    send_images: bool = True
    save_images: bool = False
    alwayson_scripts: Dict[str, Any] = field(default_factory=dict)
    infotext: str = ""


@dataclass
class AutoModelLoad(BaseRequest):
    sd_model_checkpoint: str = "sdxl/juggernautXL_v9Rundiffusionphoto2.safetensors"
