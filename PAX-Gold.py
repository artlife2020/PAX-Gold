```python
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List
import json
import logging
import uuid


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)


@dataclass
class NetworkProfile:
    name: str
    endpoint: str
    chain_id: int


@dataclass
class AccountProfile:
    address: str


class MetadataFactory:

    def __init__(self):
        self.asset = "PAX Gold"

    def build(self):

        return {
            "identifier": str(uuid.uuid4()),
            "created": datetime.utcnow().isoformat(),
            "asset": self.asset
        }


class PayloadEncoder:

    @staticmethod
    def encode(data):

        return json.dumps(
            data,
            indent=2,
            sort_keys=True
        )


class RequestBuilder:

    def __init__(
        self,
        account,
        network
    ):
        self.account = account
        self.network = network
        self.metadata = MetadataFactory()

    def create(
        self,
        contract
    ):

        return {
            "network": self.network.name,
            "chain_id": self.network.chain_id,
            "from": self.account.address,
            "to": contract,
            "value": 0,
            "metadata": self.metadata.build()
        }


class RequestValidator:

    REQUIRED = [
        "network",
        "chain_id",
        "from",
        "to",
        "value",
        "metadata"
    ]

    @classmethod
    def validate(
        cls,
        request
    ):

        for item in cls.REQUIRED:
            if item not in request:
                raise ValueError(
                    f"Missing field: {item}"
                )

        return True


class ActivityLog:

    def __init__(self):
        self.records: List[str] = []

    def add(
        self,
        message
    ):

        self.records.append(
            message
        )

    def display(self):

        print()

        for item in self.records:
            print(item)

        print()


class InteractionSession:

    def __init__(
        self,
        network,
        account
    ):
        self.network = network
        self.account = account

    def prepare(
        self,
        contract
    ):

        builder = RequestBuilder(
            self.account,
            self.network
        )

        request = builder.create(
            contract
        )

        RequestValidator.validate(
            request
        )

        return request

    def sign_transaction(
        self,
        request
    ):
        raise NotImplementedError(
            "Signing is intentionally omitted."
        )


class Reporter:

    @staticmethod
    def show(
        request
    ):

        print(
            PayloadEncoder.encode(
                request
            )
        )


def load_network():

    return NetworkProfile(
        name="Educational Network",
        endpoint="https://example.invalid",
        chain_id=0
    )


def load_account():

    return AccountProfile(
        address="0xABCDEF1234567890ABCDEF1234567890ABCDEF12"
    )


def initialize_log():

    log = ActivityLog()

    log.add(
        "Configuration loaded"
    )

    log.add(
        "Metadata initialized"
    )

    log.add(
        "Interaction request prepared"
    )

    return log


def print_summary(
    network,
    account
):

    print("Summary")
    print("-" * 30)
    print("Network :", network.name)
    print("Endpoint:", network.endpoint)
    print("Chain ID:", network.chain_id)
    print("Account :", account.address)


def main():

    logging.info(
        "Starting application"
    )

    network = load_network()

    account = load_account()

    session = InteractionSession(
        network,
        account
    )

    request = session.prepare(
        "0x1234567890123456789012345678901234567890"
    )

    Reporter.show(
        request
    )

    log = initialize_log()

    log.display()

    print_summary(
        network,
        account
