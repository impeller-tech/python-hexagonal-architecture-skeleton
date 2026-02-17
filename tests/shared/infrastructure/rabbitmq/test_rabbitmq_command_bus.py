import json
from dataclasses import dataclass
from typing import Any

import pytest

from src.shared.domain.command import Command
from src.shared.infrastructure.rabbitmq import rabbitmq_command_bus
from src.shared.infrastructure.rabbitmq.rabbitmq_command_bus import RabbitMQCommandBus


@dataclass(frozen=True)
class PublishInvoiceCommand(Command):
    invoice_id: str
    total_cents: int

    def to_payload(self) -> dict[str, Any]:
        return {"invoice_id": self.invoice_id, "total_cents": self.total_cents}


class _FakeBasicProperties:
    def __init__(self, *, content_type: str, delivery_mode: int):
        self.content_type = content_type
        self.delivery_mode = delivery_mode


class _FakeChannel:
    def __init__(self) -> None:
        self.declared: list[dict[str, Any]] = []
        self.published: list[dict[str, Any]] = []

    def queue_declare(self, *, queue: str, durable: bool) -> None:
        self.declared.append({"queue": queue, "durable": durable})

    def basic_publish(
        self,
        *,
        exchange: str,
        routing_key: str,
        body: str,
        properties: _FakeBasicProperties,
    ) -> None:
        self.published.append(
            {
                "exchange": exchange,
                "routing_key": routing_key,
                "body": body,
                "properties": properties,
            }
        )


class _FakeConnection:
    def __init__(self, connection_params: dict[str, Any]) -> None:
        self.connection_params = connection_params
        self._channel = _FakeChannel()

    def channel(self) -> _FakeChannel:
        return self._channel


class _FakePikaModule:
    BasicProperties = _FakeBasicProperties

    @staticmethod
    def ConnectionParameters(**kwargs: Any) -> dict[str, Any]:
        return kwargs

    @staticmethod
    def BlockingConnection(connection_params: dict[str, Any]) -> _FakeConnection:
        return _FakeConnection(connection_params)


def test_dispatch_publishes_json_with_persistent_properties(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rabbitmq_command_bus, "_load_pika", lambda: _FakePikaModule)

    bus = RabbitMQCommandBus(
        connection_params={"host": "localhost", "port": 5672},
        queue_name="billing.commands",
    )

    assert bus.channel.declared == [{"queue": "billing.commands", "durable": True}]

    bus.dispatch(PublishInvoiceCommand(invoice_id="inv-1", total_cents=1234))

    assert len(bus.channel.published) == 1
    published = bus.channel.published[0]
    assert published["exchange"] == ""
    assert published["routing_key"] == "billing.commands"
    assert json.loads(published["body"]) == {
        "type": "PublishInvoiceCommand",
        "data": {"invoice_id": "inv-1", "total_cents": 1234},
    }
    assert published["properties"].content_type == "application/json"
    assert published["properties"].delivery_mode == 2


def test_dispatch_rejects_non_serializable_payload(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rabbitmq_command_bus, "_load_pika", lambda: _FakePikaModule)

    @dataclass(frozen=True)
    class BadCommand(Command):
        def to_payload(self) -> dict[str, Any]:
            return {"bad": {1, 2, 3}}

    bus = RabbitMQCommandBus(connection_params={"host": "localhost"})

    with pytest.raises(ValueError, match="JSON serializable"):
        bus.dispatch(BadCommand())


def test_missing_optional_pika_dependency_message(monkeypatch: pytest.MonkeyPatch) -> None:
    def _raise_module_not_found(_name: str) -> Any:
        raise ModuleNotFoundError("No module named 'pika'")

    monkeypatch.setattr(rabbitmq_command_bus, "import_module", _raise_module_not_found)

    with pytest.raises(ModuleNotFoundError, match="optional 'pika' dependency"):
        rabbitmq_command_bus._load_pika()
