"""Import basic library files for making convenient use of the library
possible.
"""
__version__ = '0.11'

# flake8 doesn't like these imports, but they are needed for other repos
from addml.base import *  # noqa: F401,F403
from addml.flatfiles import *  # noqa: F401,F403
from addml.split_addml import *  # noqa: F401,F403
