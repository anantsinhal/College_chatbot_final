"""Process-local conversation threads for resumable Streamlit chats."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from threading import RLock
from uuid import uuid4


@dataclass
class ThreadState:
    thread_id: str
    title: str = "New Chat"
    messages: list[dict] = field(default_factory=list)
    chat_history: list[tuple[str, str]] = field(default_factory=list)
    updated_at: datetime = field(default_factory=datetime.now)


_THREADS: dict[str, ThreadState] = {}
_LOCK = RLock()


def create_thread() -> ThreadState:
    with _LOCK:
        thread = ThreadState(thread_id=str(uuid4()))
        _THREADS[thread.thread_id] = thread
        return deepcopy(thread)


def get_thread(thread_id: str) -> ThreadState | None:
    with _LOCK:
        thread = _THREADS.get(thread_id)
        return deepcopy(thread) if thread else None


def list_threads() -> list[ThreadState]:
    with _LOCK:
        return sorted(
            (deepcopy(thread) for thread in _THREADS.values()),
            key=lambda thread: thread.updated_at,
            reverse=True,
        )


def save_thread(
    thread_id: str,
    messages: list[dict],
    chat_history: list[tuple[str, str]],
) -> None:
    with _LOCK:
        thread = _THREADS.get(thread_id)
        if thread is None:
            thread = ThreadState(thread_id=thread_id)
            _THREADS[thread_id] = thread

        if not thread.title or thread.title == "New Chat":
            first_user_message = next(
                (
                    message["content"]
                    for message in messages
                    if message.get("role") == "user"
                ),
                "",
            )
            if first_user_message:
                thread.title = first_user_message.strip()[:32]

        thread.messages = deepcopy(messages)
        thread.chat_history = deepcopy(chat_history)
        thread.updated_at = datetime.now()


def delete_thread(thread_id: str) -> None:
    with _LOCK:
        _THREADS.pop(thread_id, None)
