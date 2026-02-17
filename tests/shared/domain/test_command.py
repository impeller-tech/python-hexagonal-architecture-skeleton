from dataclasses import dataclass
from typing import Any

import pytest

from src.shared.domain.command import Command


@dataclass(frozen=True)
class CreateTaskCommand(Command):
    task_id: str
    title: str

    def to_payload(self) -> dict[str, Any]:
        return {"task_id": self.task_id, "title": self.title}


def test_sample_command_to_payload() -> None:
    command = CreateTaskCommand(task_id="task-1", title="Write tests")

    assert command.to_payload() == {"task_id": "task-1", "title": "Write tests"}


def test_command_requires_payload_implementation() -> None:
    class IncompleteCommand(Command):
        pass

    with pytest.raises(TypeError):
        IncompleteCommand()
