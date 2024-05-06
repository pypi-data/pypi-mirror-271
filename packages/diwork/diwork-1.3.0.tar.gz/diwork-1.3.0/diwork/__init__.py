# -*- coding: utf-8 -*-

import os
import sys

__WORK_DIR = os.path.dirname(__file__)
sys.path.insert(0, __WORK_DIR)

sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/diwork_ways"))
sys.path.insert(0, os.path.abspath(f"{__WORK_DIR}/diwork_mains"))

from .__version__ import __version__
from .main import main

__all__ = ["__version__", main]
