"""Build-backend API."""

# Export default setuptools.build_meta hooks
from setuptools.build_meta import *  # type: ignore

# Override build_wheel hook
from ._backend import build_wheel
