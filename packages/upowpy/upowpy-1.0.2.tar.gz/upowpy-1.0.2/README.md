# upowpy Library

`upowpy` is a Python library for interacting with uPow blockchain transactions, including sending funds, staking, voting, and managing nodes and validators on the blockchain.

## Installation

```bash
pip install upowpy
```

## Usage

To use the library, you will need to have an active blockchain key and appropriate addresses for transactions.

### Example Functions

Here are some of the key functions and their usage in the `upowpy` library.

#### Send Transaction

Send a specified amount to a given address.

```python
import asyncio
import upowpy as upow

KEY = "hexKey"
TO = "wallet_address"
VOTE_TO = "wallet_address"
REVOKE_FROM = "wallet_address"
AMOUNT = "1"
VOTING_RANGE = "10"

async def send_transaction():
    try:
        transaction_hash = await upow.send_transaction(KEY, TO, AMOUNT)
        print("Transaction hash:", transaction_hash)
    except Exception as e:
        print("Failed to send transaction:", str(e))

asyncio.run(send_transaction())
```

#### Stake and Unstake Transaction

Stake or unstake an amount on the blockchain.

```python
async def stake_transaction():
    transaction_hash = await upow.stake_transaction(KEY, AMOUNT)
    print("Transaction hash:", transaction_hash)

async def unstake_transaction():
    transaction_hash = await upow.unstake_transaction(KEY)
    print("Transaction hash:", transaction_hash)
```

#### Register and Deregister Inode

Register or deregister an inode on the blockchain.

```python
async def register_inode_transaction():
    transaction_hash = await upow.register_inode_transaction(KEY)
    print("Transaction hash:", transaction_hash)

async def deregister_inode_transaction():
    transaction_hash = await upow.deregister_inode_transaction(KEY)
    print("Transaction hash:", transaction_hash)
```

#### Register Validator

Register a validator on the blockchain.

```python
async def register_validator_transaction():
    transaction_hash = await upow.register_validator_transaction(KEY)
    print("Transaction hash:", transaction_hash)
```

#### Voting and Revoking

Vote for or revoke a vote for a validator using a specified range.

```python
async def vote_transaction():
    transaction_hash = await upow.vote_transaction(KEY, VOTING_RANGE, VOTE_TO)
    print("Transaction hash:", transaction_hash)

async def revoke_transaction():
    transaction_hash = await upow.revoke_transaction(KEY, REVOKE_FROM)
    print("Transaction hash:", transaction_hash)
```

### Running the Code

You can run the asynchronous functions using the asyncio library.

```python
import asyncio

async def main():
    await send_transaction()
    # You can uncomment the below lines to perform other transactions.
    # await stake_transaction()
    # await unstake_transaction()
    # await register_inode_transaction()
    # await deregister_inode_transaction()
    # await register_validator_transaction()
    # await vote_transaction()
    # await revoke_transaction()

asyncio.run(main())
```

---
