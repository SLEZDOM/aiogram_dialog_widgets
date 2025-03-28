from typing import Dict, Optional

from aiogram.types import InlineKeyboardButton

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd.base import Keyboard
from aiogram_dialog.widgets.common import WhenCondition
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.text import Text, Const


EMPTY_TEXT = Const("")


class SwitchInlineQueryCurrentChat(Keyboard):
    def __init__(
        self,
        text: Text,
        switch_inline_query: Optional[Text] = EMPTY_TEXT,
        id: Optional[str] = None,
        when: WhenCondition = None,
    ):
        super().__init__(id=id, when=when)
        self.text = text
        self.switch_inline_query = switch_inline_query

    async def _render_keyboard(
        self,
        data: Dict,
        manager: DialogManager,
    ) -> RawKeyboard:
        return [
            [
                InlineKeyboardButton(
                    text=await self.text.render_text(data, manager),
                    switch_inline_query_current_chat=await self.switch_inline_query.render_text(data, manager),
                ),
            ],
        ]
