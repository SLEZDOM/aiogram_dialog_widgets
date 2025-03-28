from collections.abc import Callable
from operator import itemgetter
from typing import Any, Union

from magic_filter import MagicFilter

ItemGetter = Callable[[dict], Any]
ItemGetterVariant = Union[str, ItemGetter, MagicFilter]


def _get_identity(item: Any) -> ItemGetter:
    def identity(data) -> Any:
        return item

    return identity


def _get_magic_getter(f: MagicFilter) -> ItemGetter:
    def item_magic(
        data: dict,
    ) -> Any:
        return f.resolve(data)

    return item_magic


def get_item_getter(attr_val: ItemGetterVariant) -> ItemGetter:
    if isinstance(attr_val, str):
        return itemgetter(attr_val)
    elif isinstance(attr_val, MagicFilter):
        return _get_magic_getter(attr_val)
    else:
        return _get_identity(attr_val)
