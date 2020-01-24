from tcod.console import Console
from typing import List, Callable, Optional
import config as CFG


class ListMenuElement:
    def __init__(self, label: str, callback: Callable = None, *args, **kwargs):
        self.label = label
        self.cb = callback if callback is not None else ListMenuElement.default_activation_handler
        self.args = args
        self.kwargs = kwargs

    def activate(self) -> None:
        if self.cb is not None:
            self.cb(*self.args, **self.kwargs)
        else:
            if CFG.DEBUG_MODE:
                print("No callback set for ListMenuElement: activate() has no effect.")

    @staticmethod
    def default_activation_handler(*args, **kwargs) -> None:
        if CFG.DEBUG_MODE:
            print("Default callback called!")

    def set_callback(self, fn: Callable) -> "ListMenuElement":
        self.cb = fn
        return self

    # Alias for set_callback
    def set_cb(self, fn: Callable) -> "ListMenuElement":
        return self.set_callback(fn)

    def set_args(self, args) -> "ListMenuElement":
        self.args = args
        return self

    def set_kwargs(self, kwargs) -> "ListMenuElement":
        self.kwargs = kwargs
        return self


class ListMenu:
    def __init__(self, console: Console):
        self.console = console
        self.is_active = False
        self.is_hidden = False
        self.selected_element_index = 0
        self.elements: List[ListMenuElement] = []

    def get_elements_count(self) -> int:
        return len(self.elements)

    def get_selected_element(self) -> Optional[ListMenuElement]:
        if len(self.elements) > 0:
            return self.elements[self.selected_element_index]
        else:
            return None

    def select_next_element(self) -> Optional[ListMenuElement]:
        if not self.is_active:
            return self.get_selected_element()

        self.selected_element_index += 1
        if self.selected_element_index >= self.get_elements_count():
            self.selected_element_index = 0

        return self.get_selected_element()

    def select_previous_element(self) -> Optional[ListMenuElement]:
        if not self.is_active:
            return self.get_selected_element()

        if len(self.elements) > 0:
            self.selected_element_index -= 1
            if self.selected_element_index < 0:
                self.selected_element_index = self.get_elements_count() - 1

        return self.get_selected_element()

    def activate_selected_element(self) -> None:
        element: ListMenuElement = self.get_selected_element()
        if element is not None:
            element.activate()

    def add_existing_element(self, new_element: ListMenuElement) -> None:
        self.elements.append(new_element)

    def add_element(self, label: str, callback: Callable = None, *args, **kwargs) -> ListMenuElement:
        new_element = ListMenuElement(label, callback, *args, **kwargs)
        self.add_existing_element(new_element)
        return new_element

    def draw(self) -> None:
        if self.console.width < CFG.DRAW__MINIMUM_CONSOLE_WIDTH and CFG.DEBUG_MODE:
            raise RuntimeWarning('Warning: minimum console width to draw menu is not met!')
        if self.console.height < self.get_elements_count() and CFG.DEBUG_MODE:
            raise RuntimeWarning('Warning: Console height cannot fit all elements (TODO: scrolling)')

        count = 0
        element: ListMenuElement
        currently_selected: ListMenuElement = self.get_selected_element()
        for element in self.elements:
            if element == currently_selected:
                self.console.print(0, count, element.label, (0, 0, 0), (255, 255, 255))
            else:
                self.console.print(0, count, element.label)
            count += 1

    def set_active(self, is_active: bool) -> None:
        self.is_active = is_active

    def set_hidden(self, is_hidden: bool) -> None:
        self.is_hidden = is_hidden
