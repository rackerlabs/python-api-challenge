from easydict import EasyDict
import logging.config
import os
import yaml


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app_base = BASE_DIR
config_file = 'config/config.yaml'


def configure_logging(logging_config):
    logging.config.dictConfig(logging_config.dict_config)


def _load_config_file(config_filename):
    with open(os.path.join(app_base, config_filename)) as f:
        yaml_config = yaml.load(f.read())
    return EasyDict(yaml_config)


config = _load_config_file(config_file)

API_DEFAULT_LIMIT = int(os.environ.get('API_DEFAULT_LIMIT', '25'))
