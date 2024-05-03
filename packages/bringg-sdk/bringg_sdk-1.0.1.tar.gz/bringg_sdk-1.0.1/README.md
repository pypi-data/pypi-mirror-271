# Bringg Python SDK

## Introduction

Bringg is a SaaS platform that offers a suite of tools for enterprises to manage their logistics operations.
The Bringg Python SDK provides a simple way to integrate the Bringg platform with your Python application.

## Installation

To install the Bringg Python SDK, simply run the following command:

```bash
pip install bringg_sdk
```

## Getting Started

To get started, you will need to have an account on the [Bringg fleet platform](https://fleet.bringg.com).
Once you have created an account, you will need to generate an API key.

## API Reference

The Bringg Python SDK provides a simple interface to interact with the Bringg API.
The SDK provides the following classes:

### Client Classes

- `BringgClient`: The main class that is used to interact with the Bringg API.

### Model Classes

- `Task`: A class that represents a task in the Bringg system.
- `WayPoint`: A class that represents a waypoint in the Bringg system.
- `TaskInventory`: A class that represents a task inventory in the Bringg system.
- `Customer`: A class that represents a customer in the Bringg system.
- `Inventory`: A class that represents an inventory in the Bringg system.
- `NoteTypes`: A class that represents a note type in the Bringg system.
- `TaskNote`: A class that represents a task note in the Bringg system.

### Request Classes

- `BringgRequest`: A class that represents a non-authorized request to the Bringg API.
  That can be used for getting token as example.
- `AuthorizedBringgRequest`: A class that represents an authorized request to the Bringg API.

### Response Classes

- `BringgResponse`: A class that represents a response from the Bringg API.
- `GetTokenResponse`: A class that represents a response from the Bringg API that contains a token.
- `BringgResponseWithSuccessParameter`: A class that represents a response from the Bringg API that contains a success
  parameter.

### Exceptions Classes

- `BringgException`: A class that represents an exception that is thrown when an error occurs while interacting with the
  Bringg API.

## Examples

Here are some examples of how to use the Bringg Python SDK:

## FAQs / Troubleshooting

If you have any questions or issues, please refer to the [Bringg documentation](https://docs.bringg.com/).
If you are unable to find the information you need, please contact Bringg support.

## Contribution Guidelines

If you would like to contribute to the Bringg Python SDK, please fork the repository and submit a pull request.
Please ensure that your code follows the PEP 8 style guide and includes unit tests.

## TODO

- [ ] Implement all the endpoints in the Bringg API
- [ ] Write unit tests for all the classes.
- [ ] Add more examples to the README file.
- [ ] Add more documentation to the code.
- [ ] Improve the README.md file.

## License

The Bringg Python SDK is released under the MIT License. See [LICENSE](LICENSE) for more information.


