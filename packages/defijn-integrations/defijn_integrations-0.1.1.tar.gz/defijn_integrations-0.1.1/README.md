# defijn-integrations

`defijn-integrations` is a Python package providing convenient integrations with several third-party services including GitLab, Everhour, and ClickUp. This package simplifies the process of interacting with these services by wrapping their APIs into easy-to-use Python functions.

## Features

- **GitLab Integration**: Manage and interact with GitLab resources like users, groups, and projects directly from your Python code.
- **Everhour Integration**: Track time, manage tasks, and retrieve project details seamlessly.
- **ClickUp Integration**: Interface with ClickUp to manage tasks, spaces, and more.

## Installation

Install `defijn-integrations` using pip:

```bash
pip install defijn-integrations
```

If using Poetry:
    
```bash
poetry add defijn-integrations
```

## Usage

```python
from defijn_integrations.gitlabint import *
from defijn_integrations.everhourint import *
from defijn_integrations.clickupint import *
```

## Building and Publishing

To build and publish `defijn-integrations` to PyPI, follow these steps using Poetry:

### Building the Package

1. Navigate to the root directory of the project.
2. Run the following command to build your package:

    ```bash
    poetry build
    ```

    This command will generate the distribution package in the `dist` directory.

### Publishing the Package

1. Setting up Authentication for PyPI

   Before you can publish packages to PyPI, you need to authenticate your package upload requests. You can do this by creating a .pypirc file in your home directory with the following content:
    
   ```ini
   [distutils]
   index-servers =
     pypi
   
   [pypi]
   repository = https://upload.pypi.org/legacy/
   username = __token__
   password = <your-token>
   ```
    
   Replace `<your-token>` with your PyPI token.

2. Run the following command to publish your package:

   ```bash
    twine upload dist/*
   ```

    This command will publish your package to PyPI.