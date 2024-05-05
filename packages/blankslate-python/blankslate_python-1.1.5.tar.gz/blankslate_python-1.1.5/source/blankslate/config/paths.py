"""paths.py: Contains paths for the application."""

import os


class Paths:
    """
    Paths for the application.

    Notes
    -----
    This class contains paths used throughout the application.
    By storing paths in a single location, it is easier to
    manage and update them. Paths should be defined as class
    attributes and should be named in uppercase with underscores
    separating words.
    """

    # Path to the root directory of the package
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SOURCE_DIR = os.path.join(BASE_DIR, "source", "blankslate")

    # Path to the templates directory
    TEMPLATES_PATH = os.path.join(SOURCE_DIR, "generation", "templates")
