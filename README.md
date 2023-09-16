# Koala

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![PyPI license](https://img.shields.io/pypi/l/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
  - [Create Expense](#create-expense)
  - [Import Expenses](#import-expenses)
- [Supported Banks for PDF Import](#supported-banks-for-pdf-import)
- [Code Structure](#code-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

Koala is a comprehensive solution for managing your expenses. It provides a Command Line Interface (CLI) for creating and importing expenses. The application is built using Python and follows the Clean Architecture principles.

## Architecture

The application is structured based on the Clean Architecture pattern. It is divided into the following layers:

- **Entities**: Contains the business objects of the application.
- **Use Cases**: Contains application-specific business rules.
- **Interfaces**: Contains interface definitions for the adapters.
- **Adapters**: Contains the code to connect the application to external concerns.
- **Entrypoints**: Contains the entry points to the application (CLI in this case).

## Installation

To install the application, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/AlexandreSenpai/koala.git
    ```

2. Navigate to the project directory:
    ```bash
    cd koala
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Create Expense

To create an expense, run the following command:

```bash
python main.py create-expense
```

Follow the prompts to enter the expense details.

### Import Expenses

To import expenses from a PDF, run the following command:

```bash
python main.py import-expenses
```

Follow the prompts to select the PDF and confirm the expenses to be imported.

## Supported Banks for PDF Import
The application currently supports importing expenses from credit card statements in PDF format from the following banks:

- Nubank
- C6 Bank

## Code Structure
- `application/`: Contains use cases and parsers.
- `domain/`: Contains domain entities and business logic.
- `infra/`: Contains all the adapters like database and CLI.
- `main.py`: Entry point for the CLI.

## Testing
To run tests, execute the following command:

```bash
pytest
```

## Contributing
If you'd like to contribute, please fork the repository and use a feature branch. Pull requests are warmly welcome.

## License
The project is licensed under the MIT license. See LICENSE for details.

`Feel free to copy and use it for your project!` For more details, please refer to the code documentation and comments. Feel free to raise an issue for any clarifications.
