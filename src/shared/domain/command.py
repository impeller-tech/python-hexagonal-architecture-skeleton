from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

CommandT = TypeVar("CommandT", bound="Command")


class Command(ABC):
    """Base class for all commands."""

    @abstractmethod
    def to_payload(self) -> dict[str, Any]:
        """Return a JSON-serializable payload representation."""


class CommandHandler(Generic[CommandT], ABC):
    """Base class for all command handlers."""

    @abstractmethod
    def handle(self, command: CommandT) -> None:
        """Handle the command."""


class CommandBus(ABC):
    """Command bus interface."""

    @abstractmethod
    def dispatch(self, command: Command) -> None:
        """Dispatch a command to its handler."""
