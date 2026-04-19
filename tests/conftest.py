import json
import os

import pytest
import eth_tester
from eth_tester import EthereumTester, PyEVMBackend
from web3 import Web3
from web3.providers.eth_tester import EthereumTesterProvider

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEPOSIT_CONTRACT_JSON = os.path.join(ROOT, "deposit_contract.json")

MIN_DEPOSIT_AMOUNT = 1_000_000_000  # Gwei
FULL_DEPOSIT_AMOUNT = 32_000_000_000  # Gwei
DEPOSIT_CONTRACT_TREE_DEPTH = 32


def get_deposit_contract_json():
    with open(DEPOSIT_CONTRACT_JSON) as f:
        return json.load(f)


@pytest.fixture
def tester():
    return EthereumTester(PyEVMBackend())


@pytest.fixture
def a0(tester):
    return tester.get_accounts()[0]


@pytest.fixture
def w3(tester):
    return Web3(EthereumTesterProvider(tester))


@pytest.fixture
def registration_contract(w3):
    artifact = get_deposit_contract_json()
    contract = w3.eth.contract(abi=artifact["abi"], bytecode=artifact["bytecode"])
    tx_hash = contract.constructor().transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return w3.eth.contract(address=receipt.contractAddress, abi=artifact["abi"])


@pytest.fixture
def assert_tx_failed(tester):
    def _assert_tx_failed(fn, exception=eth_tester.exceptions.TransactionFailed):
        snapshot_id = tester.take_snapshot()
        with pytest.raises(exception):
            fn()
        tester.revert_to_snapshot(snapshot_id)

    return _assert_tx_failed
