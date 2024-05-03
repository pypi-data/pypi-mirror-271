# ruff: noqa: D100, D101, D102, D103, D104, D107, N999
from __future__ import annotations

import sys
from dataclasses import field
from datetime import UTC, datetime
from enum import StrEnum, auto
from typing import TYPE_CHECKING
from uuid import uuid4

from immutable import Immutable
from redux import BaseAction, BaseEvent

if TYPE_CHECKING:
    from collections.abc import Sequence


class Importance(StrEnum):
    CRITICAL = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()


IMPORTANCE_ICONS = {
    Importance.CRITICAL: '󰅚',
    Importance.HIGH: '󰀪',
    Importance.MEDIUM: '',
    Importance.LOW: '󰌶',
}

IMPORTANCE_COLORS = {
    Importance.CRITICAL: '#D32F2F',
    Importance.HIGH: '#FFA000',
    Importance.MEDIUM: '#FFEB3B',
    Importance.LOW: '#2196F3',
}


class NotificationDisplayType(StrEnum):
    NOT_SET = auto()
    BACKGROUND = auto()
    FLASH = auto()
    STICKY = auto()


def default_icon() -> str:
    # WARNING: Dirty hack ahead
    # This is to set the default value of `icon` based on the provided/default value of
    # `importance`
    parent_frame = sys._getframe().f_back  # noqa: SLF001
    if not parent_frame:
        return ''
    return IMPORTANCE_ICONS[parent_frame.f_locals.get('importance', Importance.LOW)]


def default_color() -> str:
    # WARNING: Dirty hack ahead
    # This is to set the default value of `color` based on the provided/default value of
    # `importance`
    parent_frame = sys._getframe().f_back  # noqa: SLF001
    if not parent_frame:
        return ''
    return IMPORTANCE_COLORS[parent_frame.f_locals.get('importance', Importance.LOW)]


class Chime(StrEnum):
    ADD = 'add'
    DONE = 'done'
    FAILURE = 'failure'
    VOLUME_CHANGE = 'volume'


class Notification(Immutable):
    id: str = field(default_factory=lambda: uuid4().hex)
    title: str
    content: str
    extra_information: str | None = None
    importance: Importance = Importance.LOW
    chime: Chime = Chime.DONE
    timestamp: datetime = field(default_factory=lambda: datetime.now(tz=UTC))
    is_read: bool = False
    sender: str | None = None
    actions: list[BaseAction | BaseEvent] = field(default_factory=list)
    icon: str = field(default_factory=default_icon)
    color: str = field(default_factory=default_color)
    expiry_date: datetime | None = None
    display_type: NotificationDisplayType = NotificationDisplayType.NOT_SET
    flash_time: float = 4


class NotificationsAction(BaseAction): ...


class NotificationsAddAction(NotificationsAction):
    notification: Notification


class NotificationsClearAction(NotificationsAction):
    notification: Notification


class NotificationsClearAllAction(NotificationsAction): ...


class NotificationsEvent(BaseEvent): ...


class NotificationsClearEvent(NotificationsEvent):
    notification: Notification


class NotificationsDisplayEvent(NotificationsEvent):
    notification: Notification


class NotificationsState(Immutable):
    notifications: Sequence[Notification]
    unread_count: int
