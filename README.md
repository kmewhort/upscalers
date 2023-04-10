# Upscalers

## About

This library wraps implementations of several popular image and video upscalers, aiming to make upscaling via any of these methods possible with a line of code.


## Dependencies

```
basicsr
einops
piexif
ldm
numpy
Pillow
realesrgan
Roboto
safetensors
timm==0.4.12
torch
```


## Installation


```bash
pip install upscalers
```

## Usage


```python
from upscalers import upscale

# upscale PIL image
scale_factor = 4.0
result = upscale('R-ESRGAN General 4xV3', image, scale_factor)
```

### Listing Available Upscalers

```python
# Enter in Python Interactive or run from a .py file

from upscalers import available_models

available_models()
```


```bash
# Shell Output

> [
 'Lanczos',
 'Nearest',
 'ESRGAN_4x',
 'ScuNET',
 'ScuNET PSNR',
 'SwinIR_4x',
 'R-ESRGAN General 4xV3',
 'R-ESRGAN General WDN 4xV3',
 'R-ESRGAN AnimeVideo',
 'R-ESRGAN 4x+',
 'R-ESRGAN 4x+ Anime6B',
 'R-ESRGAN 2x+']
```

Sensible defaults are used for all the models. See `config.opts` for settings that are tweakable.

## Credits

Huge credit goes to [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) --
most of the code was extracted straight from there!

## License

AGPL v3.0 (following the license for AUTOMATIC1111/stable-diffusion-webui from which this was largely extracted).

