import glob
import os
import shutil
import importlib
from urllib.parse import urlparse

from basicsr.utils.download_util import load_file_from_url

from config import opts

def load_models(model_path: str, model_url: str = None, command_path: str = None, ext_filter=None, download_name=None, ext_blacklist=None) -> list:
    """
    A one-and done loader to try finding the desired models in specified directories.

    @param download_name: Specify to download from model_url immediately.
    @param model_url: If no other models are found, this will be downloaded on upscale.
    @param model_path: The location to store/find models in.
    @param command_path: A command-line argument to search for models in first.
    @param ext_filter: An optional list of filename extensions to filter by
    @return: A list of paths containing the desired model(s)
    """
    output = []

    if ext_filter is None:
        ext_filter = []

    try:
        places = []

        if command_path is not None and command_path != model_path and os.path.exists(command_path):
            places.append(command_path)

        places.append(model_path)

        for place in places:
            if os.path.exists(place):
                for file in glob.iglob(place + '**/**', recursive=True):
                    full_path = file
                    if os.path.isdir(full_path):
                        continue
                    if os.path.islink(full_path) and not os.path.exists(full_path):
                        print(f"Skipping broken symlink: {full_path}")
                        continue
                    if ext_blacklist is not None and any([full_path.endswith(x) for x in ext_blacklist]):
                        continue
                    if len(ext_filter) != 0:
                        model_name, extension = os.path.splitext(file)
                        if extension not in ext_filter:
                            continue
                    if file not in output:
                        output.append(full_path)

        if model_url is not None and len(output) == 0:
            if download_name is not None:
                dl = load_file_from_url(model_url, model_path, True, download_name)
                output.append(dl)
            else:
                output.append(model_url)

    except Exception:
        pass

    return output


def friendly_name(file: str):
    if "http" in file:
        file = urlparse(file).path

    file = os.path.basename(file)
    model_name, extension = os.path.splitext(file)
    return model_name

def load_upscalers():
    from models.upscaler import Upscaler
    # We can only do this 'magic' method to dynamically load upscalers if they are referenced,
    # so we'll try to import any _model.py files before looking in __subclasses__
    for file in os.listdir(opts.upscalers_path):
        if "_model.py" in file:
            model_name = file.replace("_model.py", "")
            full_model = f"models.{model_name}_model"
            try:
                importlib.import_module(full_model)
            except:
                pass

    datas = []
    for cls in Upscaler.__subclasses__():
        name = cls.__name__
        cmd_name = f"{name.lower().replace('upscaler', '')}_models_path"
        scaler = cls(cmd_name)
        datas += scaler.scalers
    return datas
