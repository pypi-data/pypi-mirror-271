# Opmentis

Opmentis is a Python package designed to manage user registrations within a decentralized application, allowing users to register as miners or validators with AWS DynamoDB. This package simplifies the process of user registration by providing a single function that can handle different user roles based on the presence of a stake.

## Features

- **User Registration**: Simplified user registration that supports different roles (miner or validator).
- **Easy Configuration**: Configuration managed through environment variables for AWS settings.
- **Scalable and Secure**: Uses AWS DynamoDB for scalable and secure data storage.

## Installation

Install Opmentis using pip:

```bash
pip install opmentis
```

# Usage

### Registering a Miner
To register a new user as a miner:

```python
from opmentis import register_miners

# Example: Registering a miner
miner_wallet_address = "miner_wallet_address"
miner = register_miners(wallet_address=miner_wallet_address)
print("Miner Registered:", miner)

```

### Contributing
Contributions to Opmentis are welcome. Please fork the repository, make your changes, and submit a pull request.

### License


For more information and updates, visit GitHub repository URL or contact the project maintainers.

