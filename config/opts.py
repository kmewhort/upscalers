import os
import sys
import torch

# 
# General
#

# Paths
config_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
upscalers_path = os.path.join(config_path, "models")
models_path = os.path.join(config_path, ".model_cache")

# Progess output
progress_print_out = sys.stdout

#
# Device
#
device = 'cuda'
# Disable half-precision
no_half = False
# channels last
channels_last = False
dtype = torch.float16

# whether to keep the models loaded in memory between upscale calls
cache_models_on_device = True

#
# Upscaler config
#


# When not using half-precision, can improve performance with less memory 
upcast_sampling = False

# Tile size for SWIN
swin_tile_size = 192 
swin_tile_overlap = 8 # Low values = visible seam
