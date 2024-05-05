# Blankslate

![Continuous Integration (CI) Tests](https://github.com/unkokaeru/blankslate/actions/workflows/continuous_integration.yml/badge.svg)

Blankslate automates the creation of Python projects, ensuring that every detail adheres to the best practices of Python development. It leverages GitHub Actions, NumPy docstrings, and a well-organised directory structure to deliver a ready-to-deploy project scaffold.

## Installation

To install Blankslate, simply run:

```bash
pip install blankslate
```

## Getting Started

After installation, you can create a new project by executing:

```bash
blankslate
```

Follow the prompts to specify your project details. Blankslate will create the project in your designated directory. You can then push this project to GitHub and start programming in the `source/PROJECT_NAME/` directory.

## Features

- **Automatic Project Structure Creation**: Sets up a GitHub-ready Python project with best practices.
- **Semantic Versioning**: Use the script `./scripts/release.sh VERSION_NUMBER` to auto-version and generate a changelog. Ensure `VERSION_NUMBER` follows [semantic versioning](https://semver.org).
- **Commit Style**: Commits should follow the [Angular commit style](https://gist.github.com/brianclements/841ea7bffdb01346392c#commit-message-header).
- **Documentation**: Automatically generates and pushes documentation to GitHub pages. Make sure your GitHub repository is configured under `Settings -> Pages`.
- **TODO to GitHub Issues**: Converts `# TODO` comments in your Python code into GitHub issues. Configure this in `Settings -> Actions (General) -> Workflow permissions` and enable "Read and write permissions".

## Extensions

Enhance your Blankslate experience with the [Blankslate Extension Pack](https://marketplace.visualstudio.com/items?itemName=unkokaeru.blankslate-extension-pack) for [VS Code](https://code.visualstudio.com/download).

## Contributing

Contributions are welcome! Please refer to our `CONTRIBUTING.md` for more information.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.