from collections.abc import Iterable
from itertools import chain, zip_longest
from typing import Optional

from aiogram.types import InlineKeyboardButton
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.api.protocols import DialogManager
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.widgets.kbd.base import Keyboard


def empty_button():
    return InlineKeyboardButton(text=" ", callback_data="empty")


class KeyboardGrid(Keyboard):
    def __init__(
        self,
        *buttons: Keyboard,
        id: Optional[str] = None,
        when: WhenCondition = None,
    ):
        super().__init__(id=id, when=when)
        self.buttons = buttons

    async def _render_keyboard(
        self,
        data: dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        kbd = []

        for button in self.buttons:
            b_kbd = await button.render_keyboard(data, manager)
            if isinstance(b_kbd, Iterable):
                kbd.append(list(chain(*b_kbd)))
    
        return [list(row) for row in zip_longest(*kbd, fillvalue=empty_button())]
