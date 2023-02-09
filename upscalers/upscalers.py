import torch
from config.modelloader import load_upscalers

UPSCALERS = load_upscalers()
AVAILABLE_MODELS = [scaler.name for scaler in UPSCALERS]

def upscale(model_name, pil_image, scale_factor):
   global UPSCALERS, AVAILABLE_MODELS
   if model_name not in AVAILABLE_MODELS:
       raise Exception(f"{model_name} is not a known model")

   upscaler = next(upscaler for upscaler in UPSCALERS if upscaler.name == model_name)
   return upscaler.scaler.upscale(pil_image, scale_factor, upscaler.data_path)

def available_models():
    global AVAILABLE_MODELS
    return AVAILABLE_MODELS

def clear_on_device_caches():
    for upscaler in UPSCALERS:
        upscaler.scaler.clear_on_device_cache()
    torch.cuda.empty_cache()
