"""paths.py: Contains paths for the application."""

import shutil
import tempfile
from importlib import resources
from pathlib import Path


class Paths:
    """
    Paths for the application.

    Notes
    -----
    This class contains paths used throughout the application.
    By storing paths in a single location, it is easier to manage and update them.
    Paths should be defined as class attributes and should be named in uppercase
    with underscores separating words.
    """

    # Create a temporary directory to store templates
    temp_dir = Path(tempfile.mkdtemp())

    # Path to the templates directory; we'll copy them to the temporary directory
    @classmethod
    def setup_templates(cls) -> None:
        # Access the package directory for templates
        templates_package = resources.files("blankslate.generation.templates")

        # Ensure the temporary directory is clear (useful for reinitialising or debugging)
        shutil.rmtree(cls.temp_dir)
        cls.temp_dir.mkdir(parents=True, exist_ok=True)

        # Copy files from the Traversable object to the temporary directory
        for template in templates_package.iterdir():
            if template.is_file():
                shutil.copy(str(template), str(cls.temp_dir))

    # Get the path to the temporary directory
    TEMPLATES_PATH = temp_dir

    # TODO: Correct temporary directory generation to follow best practices and avoid security risks


# Initialise the setup at import
Paths.setup_templates()
