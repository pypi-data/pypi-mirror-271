#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from .ernie import *  # noqa: F401, F403

__version__ = '1.2405.2'

logging.getLogger().setLevel(logging.WARNING)
logging.getLogger('transformers.tokenization_utils').setLevel(logging.ERROR)
