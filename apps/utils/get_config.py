# Third Party Module Import
from flask import current_app

# Python Module Import
import logging


def get_config(key):
    value = current_app.config.get(key)
    if value is None:
        logging.error('Not information in config')
        raise ValueError
    return value
