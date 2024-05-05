"""___main___.py: Called when the package is run as a script."""

from .generation.project_generation import generate_project
from .interface.command_line import input_project_details
from .logs.setup_logging import setup_logging

main_logger = setup_logging()


if __name__ == "__main__":
    try:
        main_logger.info("Application started.")
        project_details = input_project_details()
        generate_project(project_details)
    except KeyboardInterrupt:
        print("\n")
        main_logger.info("Exiting application due to user interrupt...")
