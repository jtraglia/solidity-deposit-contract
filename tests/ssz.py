"""Minimal SSZ types needed to compute `hash_tree_root(DepositData)` and the
`List[DepositData, 2**32]` deposit tree used in the tests.

Backed by `remerkleable`, so this module only wires together the exact types
the deposit contract cares about. Keeping them here avoids pulling in the
full `consensus-specs` package."""

from remerkleable.basic import uint64
from remerkleable.byte_arrays import ByteVector
from remerkleable.complex import Container, List as _List


class Bytes48(ByteVector[48]):
    pass


class Bytes32(ByteVector[32]):
    pass


class Bytes96(ByteVector[96]):
    pass


class DepositData(Container):
    pubkey: Bytes48
    withdrawal_credentials: Bytes32
    amount: uint64
    signature: Bytes96


DEPOSIT_CONTRACT_TREE_DEPTH = 32
DepositDataList = _List[DepositData, 2**DEPOSIT_CONTRACT_TREE_DEPTH]


def hash_tree_root(value) -> bytes:
    return bytes(value.hash_tree_root())
