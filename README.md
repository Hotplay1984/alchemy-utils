# Alchemy Utils

A collection of utility functions and tools for the Alchemy project.

## Features

- `config_utils.py`: A flexible configuration parser that supports multiple config file locations and environment variables
- `setup.py`: Package setup and dependency management

## Installation

```bash
pip install -e .
```

## Usage

```python
from utils.config_utils import ConfigParser

# Initialize config parser
config = ConfigParser(
    env_var_name="CONFIG_PATH",
    user_config_paths="~/.config/myapp/config.ini",
    system_config_paths="/etc/myapp/config.ini"
)

# Parse config file
config_dict = config.parse()
```

## Author

[Hotplay1984](https://github.com/Hotplay1984) 