""" This file is used to import the settings file based on the environment variable DEBUG. """

import os

if os.environ.get("DEBUG"):
    from .local import *
else:
    from .production import *
