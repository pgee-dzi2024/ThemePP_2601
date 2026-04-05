from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Dict

from .transcription_service import transcribe_media_file

EXECUTOR = ThreadPoolExecutor(max_workers=2)
TASKS: dict[str, dict[str, Any]] = {}


def create_task(file_path: Path) -> str:
    task_id = uuid.uuid4().hex

    TASKS[task_id] = {
        "status": "pending",
        "result": None,
        "error": None,
    }

    future = EXECUTOR.submit(_run_task, task_id, file_path)
    TASKS[task_id]["future"] = future
    return task_id


def _run_task(task_id: str, file_path: Path) -> None:
    try:
        TASKS[task_id]["status"] = "processing"
        result = transcribe_media_file(file_path)
        TASKS[task_id]["status"] = "done"
        TASKS[task_id]["result"] = result
    except Exception as exc:
        TASKS[task_id]["status"] = "error"
        TASKS[task_id]["error"] = str(exc)
    finally:
        TASKS[task_id].pop("future", None)


def get_task(task_id: str) -> dict[str, Any] | None:
    return TASKS.get(task_id)