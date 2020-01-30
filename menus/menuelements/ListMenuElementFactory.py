from typing import Union, Callable

from menus.menuelements.CallbackListMenuElement import CallbackListMenuElement
from menus.menuelements.NumericListMenuElement import NumericListMenuElement
from .ListMenuElementEnum import ListMenuElementEnum as ElementType


class ListMenuElementFactory:
    @staticmethod
    def create_list_menu_element(element_type: ElementType, label: str, *args, **kwargs) -> Union[CallbackListMenuElement, NumericListMenuElement]:
        if element_type == ElementType.NUMERIC:
            return ListMenuElementFactory.__create_numeric_list_menu_element_from_argskwargs(label, *args, **kwargs)

        elif element_type == ElementType.CALLBACK:
            return ListMenuElementFactory.__create_callback_list_menu_element_from_argskwargs(label, *args, **kwargs)

    @staticmethod
    def __create_numeric_list_menu_element_from_argskwargs(label: str, *args, **kwargs):
        initial_value = 0.0

        if len(args) >= 1:  # ignore the rest of the args
            try:
                initial_value = float(args[0])
                initial_value = int(initial_value) if initial_value.is_integer() else initial_value
            except ValueError:
                initial_value = 0

        if 'initial_value' in kwargs:
            try:
                initial_value = float(kwargs.get('initial_value'))
                initial_value = int(initial_value) if initial_value.is_integer() else initial_value
            except ValueError:
                initial_value = 0

        return NumericListMenuElement(label, initial_value)

    @staticmethod
    def create_numeric_list_menu_element(label: str, initial_value: Union[int, float]) -> NumericListMenuElement:
        return NumericListMenuElement(label, initial_value)

    @staticmethod
    def __create_callback_list_menu_element_from_argskwargs(label, *args, **kwargs) -> CallbackListMenuElement:
        callback = None

        if 'callback' in kwargs:
            callback = kwargs.get('callback') if callable(kwargs.get('callback')) else None

        if len(args) >= 1 and callback is None:
            callback = args[0] if callable(args[0]) else None
            if callback is not None:
                args = args[1:]

        return CallbackListMenuElement(label, callback, *args)

    @staticmethod
    def create_callback_list_menu_element(label: str, callback: Callable, *args) -> CallbackListMenuElement:
        return CallbackListMenuElement(label, callback, *args)
