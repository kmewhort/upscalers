import os
import sys
import traceback

import numpy as np
from PIL import Image
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer

from config import opts 
from models.upscaler import Upscaler, UpscalerData

class UpscalerRealESRGAN(Upscaler):
    def __init__(self, path):
        self.name = "RealESRGAN"
        self.user_path = path
        self.outscale = None
        super().__init__()
        try:
            from basicsr.archs.rrdbnet_arch import RRDBNet
            from realesrgan import RealESRGANer
            from realesrgan.archs.srvgg_arch import SRVGGNetCompact
            self.enable = True
            self.scalers = self.load_models(path)

        except Exception:
            print("Error importing Real-ESRGAN:", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            self.enable = False
            self.scalers = []

    def do_upscale(self, img, path):
        if not self.enable:
            return img

        if self.on_device_model_cache is not None:
            upsampler = self.on_device_model_cache
        else:
            info = self.load_model(path)
            # TODO: should this actually be the same scale used for model init and .enhance? it
            # doesn't look like the actual scale is used
            self.outscale = info.scale
            if not os.path.exists(info.local_data_path):
                print("Unable to load RealESRGAN model: %s" % info.name)
                return img

            upsampler = RealESRGANer(
                scale=self.outscale,
                model_path=info.local_data_path,
                model=info.model(),
                half=not opts.no_half and not opts.upcast_sampling
            )
            if opts.cache_models_on_device:
                self.on_device_model_cache = upsampler

        upsampled = upsampler.enhance(np.array(img), outscale=self.outscale)[0]

        image = Image.fromarray(upsampled)
        return image

    def load_model(self, path):
        try:
            info = next(iter([scaler for scaler in self.scalers if scaler.data_path == path]), None)

            if info is None:
                print(f"Unable to find model info: {path}")
                return None

            info.local_data_path = load_file_from_url(url=info.data_path, model_dir=self.model_path, progress=True)
            return info
        except Exception as e:
            print(f"Error making Real-ESRGAN models list: {e}", file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
        return None

    def load_models(self, _):
        return get_realesrgan_models(self)


def get_realesrgan_models(scaler):
    try:
        from basicsr.archs.rrdbnet_arch import RRDBNet
        from realesrgan.archs.srvgg_arch import SRVGGNetCompact
        models = [
            UpscalerData(
                name="R-ESRGAN General 4xV3",
                path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
                scale=4,
                upscaler=scaler,
                model=lambda: SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
            ),
            UpscalerData(
                name="R-ESRGAN General WDN 4xV3",
                path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
                scale=4,
                upscaler=scaler,
                model=lambda: SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type='prelu')
            ),
            UpscalerData(
                name="R-ESRGAN AnimeVideo",
                path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth",
                scale=4,
                upscaler=scaler,
                model=lambda: SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type='prelu')
            ),
            UpscalerData(
                name="R-ESRGAN 4x+",
                path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
                scale=4,
                upscaler=scaler,
                model=lambda: RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
            ),
            UpscalerData(
                name="R-ESRGAN 4x+ Anime6B",
                path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
                scale=4,
                upscaler=scaler,
                model=lambda: RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
            ),
            UpscalerData(
                name="R-ESRGAN 2x+",
                path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
                scale=2,
                upscaler=scaler,
                model=lambda: RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
            ),
        ]
        return models
    except Exception as e:
        print("Error making Real-ESRGAN models list:", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
