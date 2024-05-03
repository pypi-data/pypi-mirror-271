# Standardized `setup.py`

## Overview

This project contains a Python-based setup automation tool designed to help streamline the process of preparing and managing project setups. It includes utilities for handling versioning, dates, notes, and README files, leveraging a dynamic caching system to maintain state across sessions.

## Word of Caution

:warning: **This project is still in development and should be used with caution.** :warning:

## Planned Features

- [ ] **Date Management:** Automatically manages the date of the last modification using a custom class.
- [ ] **Version Control:** Validates and stores version numbers with a strict format.
- [ ] **Notes Management:** Supports capturing and formatting release notes for easy inclusion in project documentation.
- [ ] **Automated Setup:** Integrates with `setuptools` for seamless package distribution preparation.

## Requirements

- Python 3.x
- `setuptools` module

## Usage

1. **Initialization:** Start by configuring the basic project parameters like name, version, and description.
2. **Parameter Management:** Through interactive prompts, manage various parameters including version number,
                               modification dates, and release notes.
3. **Setup Execution:** Execute the setup to generate distribution packages and, optionally, publish them to PyPi.

### Example

```python
from templated_setup import Setup_Helper

DESCRIPTION = "A quick and easy replacement for some `setup.py` implementations."

Setup_Helper.setup(
	name="templated_setup",
	author="matrikater (Joel Watson)",
	description=DESCRIPTION,
	author_email="administraitor@matriko.xyz",
)
```

## Installation

To install the package, run the following command:

```bash
pip install templated-setup
```

## Contributing

Contributions are welcome! For feature requests, bug reports, or questions, please submit an issue.

> Actually I would be happy to have some help with this project as making a `setup.py` every time is a bit boring.

## License

This project is licensed under the GPLv2 License - see the [LICENSE](LICENSE) file for details.
