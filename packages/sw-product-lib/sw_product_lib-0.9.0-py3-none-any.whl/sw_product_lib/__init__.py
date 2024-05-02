import importlib.metadata

from strangeworks_core.config.config import Config


__version__ = importlib.metadata.version("sw_product_lib")
# initialize common common objects
cfg = Config()


def in_dev_mode():
    return cfg.get_bool("dev_mode")
