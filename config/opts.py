import torch

# 
# General
#

# Paths
models_path = "./.model_cache"
config_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))
upscalers_path = config_path.join("../models")

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

#
# Upscaler config
#


# When not using half-precision, can improve performance with less memory 
upcast_sampling = False

# num steps for LDSR. lower = faster.
ldsr_steps = 100
# cache LDSR model in memory
ldsr_cached - True

# Tile size for SWIN
swin_tile_size = 192 
swin_tile_overlap = 8 # Low values = visible seam
