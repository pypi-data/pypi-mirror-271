import logging
import logging.config
import os
from pathlib import Path

import yaml


def setup_logging(
        default_path=Path(__file__).parent.joinpath('../config/logging.yaml'),
        default_level=logging.INFO,
        env_key='LOG_CFG'
):
    """Setup logging configuration

    """

    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value

    if path.exists():
        with path.open('rt') as yaml_file:
            config = yaml.safe_load(yaml_file.read())

        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)