from typing import Callable, Generic, Union

from aiogram.types import CallbackQuery, InlineKeyboardButton
from aiogram_dialog import DialogManager, DialogProtocol
from aiogram_dialog.widgets.common import ManagedWidget
from aiogram_dialog.widgets.kbd.base import Keyboard
from aiogram_dialog.widgets.kbd.select import T, OnItemClick
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.widget_event import (
    ensure_event_processor,
    WidgetEventProcessor
)


class Rating(Keyboard, Generic[T]):
    def __init__(
        self,
        checked_text: Text,
        unchecked_text: Text,
        id: str,
        default: int = 0,
        max_value: int = 5,
        on_click: Union[
            OnItemClick["Rating[T]", T],
            WidgetEventProcessor, None,
        ] = None,
        when: Union[str, Callable] = None,
    ):
        super().__init__(id=id, when=when)
        self.checked_text = checked_text
        self.unchecked_text = unchecked_text
        self.default = default
        self.max_value = max_value
        self.on_click = ensure_event_processor(on_click)

    def get_value(self, manager: DialogManager) -> int:
        return self.get_widget_data(manager, self.default)

    async def set_value(
        self,
        manager: DialogManager,
        value: int
    ) -> None:
        if 0 <= value <= self.max_value:
            currentRating: int = self.get_value(manager)

            if value == currentRating:
                return await self.reset_value(manager)

            self.set_widget_data(manager, value)

    async def reset_value(
        self,
        manager: DialogManager,
    ) -> None:
        self.set_widget_data(manager, 0)

    async def _process_item_callback(
        self,
        callback: CallbackQuery,
        data: str,
        dialog: DialogProtocol,
        manager: DialogManager,
    ) -> bool:
        value = int(data)

        await self.set_value(manager, value)

        await self.on_click.process_event(
            callback,
            self.managed(manager),
            manager,
            value
        )
        
        return True

    async def _render_keyboard(
        self,
        data,
        manager: DialogManager,
    ) -> RawKeyboard:
        buttons = []
        currentRating: int = self.get_value(manager)

        for index, _ in enumerate(range(self.max_value)):
            normalIndexValue: int = index + 1

            isFilled: bool = normalIndexValue <= currentRating

            if isFilled:
                text = await self.checked_text.render_text(data, manager)
            else:
                text = await self.unchecked_text.render_text(data, manager)

            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=self._item_callback_data(normalIndexValue),
            ))

        return [buttons]

    def managed(self, manager: DialogManager):
        return ManagedRating(self, manager)


class ManagedRating(ManagedWidget[Rating]):
    def get_value(self) -> int:
        return self.widget.get_value(self.manager)

    async def set_value(self, value: int) -> None:
        await self.widget.set_value(self.manager, value)

    async def reset_value(self) -> None:
        await self.widget.reset_value(self.manager)
