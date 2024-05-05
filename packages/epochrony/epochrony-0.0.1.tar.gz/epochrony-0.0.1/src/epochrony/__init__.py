"""
Package startup to set log level for subsequent modules.
Loads main class to make available at package level.
"""

import logging
import os

from .base import Epochrony

# Configure log level from environment
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.getLogger().setLevel(LOG_LEVEL)
logging.info("Using log level %s", LOG_LEVEL)

# Use class to avoid unused variable linting warnings
type(Epochrony)
