import logging
import requests
from .upow_transactions.helpers import sha256, string_to_bytes
from .utils.utils import Utils

wallet_utils: Utils = Utils()


async def push_tx(tx, wallet_utils: Utils):
    try:
        r = requests.get(
            f"{wallet_utils.NODE_URL}/push_tx", {"tx_hex": tx.hex()}, timeout=10
        )
        r.raise_for_status()
        res = r.json()
        if res["ok"]:
            transaction_hash = sha256(tx.hex())
            return None, transaction_hash
        else:
            return "Transaction not pushed", None
    except Exception as e:
        logging.error(f"Error during request to node: {e}")
        return str(e), None


async def send_transaction(private_key_hex, recipients, amounts, message=None):
    private_key = int(private_key_hex, 16)
    recipients_list = recipients.split(",")
    amounts_list = amounts.split(",")
    message_bytes = string_to_bytes(message) if message else None
    if (
        len(recipients_list) > 1
        and len(amounts_list) > 1
        and len(recipients_list) == len(amounts_list)
    ):
        tx = await wallet_utils.create_transaction_to_send_multiple_wallet(
            private_key, recipients_list, amounts_list, message_bytes
        )
    else:
        receiver = recipients_list[0]
        amount = amounts_list[0]
        tx = await wallet_utils.create_transaction(
            private_key, receiver, amount, message_bytes
        )
    error_message, transaction_hash = await push_tx(tx, wallet_utils)
    if transaction_hash:
        return transaction_hash
    else:
        raise Exception(error_message)


async def stake_transaction(private_key_hex, amount):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_stake_transaction(private_key, amount)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def unstake_transaction(private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_unstake_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def register_inode_transaction(private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_inode_registration_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def deregister_inode_transaction(private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_inode_de_registration_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def register_validator_transaction(private_key_hex):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_validator_registration_transaction(private_key)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def vote_transaction(private_key_hex, voting_range, recipient):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_voting_transaction(
            private_key, voting_range, recipient
        )
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise


async def revoke_transaction(private_key_hex, revoke_from):
    try:
        private_key = int(private_key_hex, 16)
        tx = await wallet_utils.create_revoke_transaction(private_key, revoke_from)
        error_message, transaction_hash = await push_tx(tx, wallet_utils)
        if transaction_hash:
            return transaction_hash
        else:
            raise Exception(error_message)
    except Exception as e:

        raise
