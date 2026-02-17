import json
from importlib import import_module
from typing import Any

from src.shared.domain.command import Command, CommandBus


def _load_pika() -> Any:
    try:
        return import_module("pika")
    except ModuleNotFoundError as exc:
        raise ModuleNotFoundError(
            "RabbitMQCommandBus requires the optional 'pika' dependency. "
            "Install it with: uv sync --extra rabbitmq"
        ) from exc

class RabbitMQCommandBus(CommandBus):
    def __init__(self, connection_params: dict[str, Any], queue_name: str = "commands"):
        pika = _load_pika()
        self._pika = pika
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(**connection_params)
        )
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def dispatch(self, command: Command) -> None:
        command_data = {
            "type": command.__class__.__name__,
            "data": command.to_payload(),
        }

        try:
            body = json.dumps(command_data)
        except TypeError as exc:
            raise ValueError("Command payload must be JSON serializable") from exc

        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=body,
            properties=self._pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
            ),
        )
