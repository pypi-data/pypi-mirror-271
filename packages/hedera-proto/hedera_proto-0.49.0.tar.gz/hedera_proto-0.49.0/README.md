# hedera-protobufs-python

Hedera API Definitions in Protocol Buffer compiled to Python

They are compiled from .proto files in [Java Protobufs](https://github.com/hashgraph/hedera-protobufs-java).

## Usage

Install:

    pip install hedera-proto

To use, just import them in your python program, e.g.:

    from hedera_proto import AccountID
    accountId = AccountID()

Or:

    import hedera_proto as proto
    accountId = proto.AccountID()

## Note

This is used by pure Python Hedera SDK, which, as of now (2021/11), has not been released yet.

You are encouraged to use the fully functional Python SDK [github.com/wensheng/hedera-sdk-py](https://github.com/wensheng/hedera-sdk-py), which is a Python wrapper around Java SDK, while waiting for pure Python SDK.
