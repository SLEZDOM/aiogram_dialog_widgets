from enum import Enum
from typing import Callable, Union

from aiogram.types import InlineKeyboardButton
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Scroll
from aiogram_dialog.widgets.kbd.pager import (
    DEFAULT_CURRENT_PAGE_TEXT,
    DEFAULT_PAGE_TEXT,
    DEFAULT_PAGER_ID,
    BasePager
)
from aiogram_dialog.api.internal import RawKeyboard
from aiogram_dialog.widgets.text import Text


class PaginationMode(Enum):
    NORMAL = "NORMAL"
    CENTERED = "CENTERED"


class Pagination(BasePager):
    def __init__(
        self,
        id: str = DEFAULT_PAGER_ID,
        scroll: Union[str, Scroll, None] = None,
        mode: PaginationMode = PaginationMode.NORMAL,
        width: int = 5,
        page_text: Text = DEFAULT_PAGE_TEXT,
        current_page_text: Text = DEFAULT_CURRENT_PAGE_TEXT,
        when: Union[str, Callable] = None,
    ):
        super().__init__(scroll=scroll, id=id, when=when)
        self.mode = mode
        self.width = width
        self.page_text = page_text
        self.current_page_text = current_page_text

    def _range_list(self, start: int, end: int) -> list[int]:
        return [i for i in range(start, end)]

    async def _prepare_data(
        self,
        data: dict,
        current_page: int,
        pages: int,
    ):
        return {
            "data": data,
            "current_page": current_page,
            "current_page1": current_page + 1,
            "pages": pages,
        }

    async def _prepare_page_data(
        self,
        data: dict,
        target_page: int,
    ):
        data = data.copy()
        data["target_page"] = target_page
        data["target_page1"] = target_page + 1
        return data

    async def _render_pages(
        self,
        pages: int,
        page: int,
        width: int,
        pagination_mode: PaginationMode
    ):
        if pagination_mode == PaginationMode.NORMAL:
            start_index = width * (page // width)
            end_index = min(pages, start_index + width)
            return self._range_list(start_index, end_index)

        elif pagination_mode == PaginationMode.CENTERED:
            half_width = width // 2
            start_index = max(0, min(page - half_width, pages - width))
            end_index = min(pages, start_index + width)
            return self._range_list(start_index, end_index)

        raise ValueError(f"Unknown pagination mode: {pagination_mode}")

    async def _render_keyboard(
        self,
        data,
        manager: DialogManager,
    ) -> RawKeyboard:
        buttons = []
        scroll = self._find_scroll(manager)
        pages = await scroll.get_page_count(data)
        current_page = await scroll.get_page()

        pager_data = await self._prepare_data(
            data=data,
            current_page=current_page,
            pages=pages,
        )

        item_list = await self._render_pages(
            pages=pages,
            page=current_page,
            width=self.width,
            pagination_mode=self.mode
        )

        for item in item_list:
            button_data = await self._prepare_page_data(
                data=pager_data,
                target_page=item,
            )

            if item == current_page:
                text_widget = self.current_page_text
            else:
                text_widget = self.page_text

            buttons.append(
                InlineKeyboardButton(
                    text=await text_widget.render_text(button_data, manager),
                    callback_data=self._item_callback_data(item),
                )
            )

        return [buttons]
