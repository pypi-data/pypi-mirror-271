"""paths.py: Contains paths for the application."""

from importlib import resources


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

    # Path to the templates directory
    with resources.path("blankslate.generation.templates", "") as templates_path:
        TEMPLATES_PATH = templates_path
