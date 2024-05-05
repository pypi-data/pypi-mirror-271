"""main.py: Enter the application."""

from .generation.project_generation import generate_project
from .interface.command_line import input_project_details
from .logs.setup_logging import setup_logging

main_logger = setup_logging()


def run_blankslate() -> None:
    """
    Main entry point of the application.

    Notes
    -----
    This function is the main entry point of the application.
    It is responsible for starting the application, taking in
    user input, and generating the project. It does not return
    anything.
    """
    main_logger.info("Application started.")

    project_details = input_project_details()

    generate_project(project_details)


if __name__ == "__main__":
    try:
        run_blankslate()
    except KeyboardInterrupt:
        print("\n")
        main_logger.info("Exiting application due to user interrupt...")
