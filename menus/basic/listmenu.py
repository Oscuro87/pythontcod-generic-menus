from tcod.console import Console
from typing import List, Callable, Optional
import config as CFG


class ListMenuElement:
    """
    A simple menu with multiple elements stacked on top of each other.
    Each element accepts a label (required), and a callback (not required)
    """

    def __init__(self, label: str, callback: Callable = None, *args, **kwargs):
        self.label = label
        self.cb = callback if callback is not None else ListMenuElement.default_activation_handler
        self.args = args
        self.kwargs = kwargs

    def activate(self) -> None:
        """
        Activates the callback currently attached to this instance of a ListMenuElement.
        If the callback is not set, nothing will happen (But a debug message when DEBUG_MODE == True)
        """
        if self.cb is not None:
            self.cb(*self.args, **self.kwargs)
        else:
            if CFG.DEBUG_MODE:
                print("No callback set for ListMenuElement: activate() has no effect.")

    @staticmethod
    def default_activation_handler(*args, **kwargs) -> None:
        """
        Don't mind this, it was just for testing purpose
        """
        if CFG.DEBUG_MODE:
            print("Default callback called!")

    def set_callback(self, fn: Callable) -> "ListMenuElement":
        """
        Chain-friendly method; sets a callback to the current instance
        :param fn: The callback to assign to this instance
        :return: Returns self, to allow chaining methods
        """
        self.cb = fn
        return self

    def set_cb(self, fn: Callable) -> "ListMenuElement":
        """
        Just an alias for the set_callback method, see above!
        """
        return self.set_callback(fn)

    def set_args(self, args) -> "ListMenuElement":
        """
        Sets the args, read by the callback when it is activated.
        Args are not required, unless needed by your callback implementation.
        :param args: The args to assign to the current instance
        :return: Returns self, to allow chaining methods
        """
        self.args = args
        return self

    def set_kwargs(self, kwargs) -> "ListMenuElement":
        """
        Sets the kwargs, read by the callback when it is activated.
        Kwargs are not required, unless needed by your callback implementation.
        :param kwargs: The kwargs to assign to the current instance
        :return: Returns self, to allow chaining methods
        """
        self.kwargs = kwargs
        return self


class ListMenu:
    def __init__(self, console: Console):
        """
        Creates a new ListMenu
        :param console: The TCOD Console you wish to draw the menu upon. It can be the root console, as well
            as a console that you blit on the root console afterwards.
        """
        self.console = console
        self.is_active = False
        self.is_hidden = False
        self.selected_element_index = 0
        self.elements: List[ListMenuElement] = []

    def get_elements_count(self) -> int:
        return len(self.elements)

    def get_selected_element(self) -> Optional[ListMenuElement]:
        """
        Gets the currently selected element of this menu
        :return: The selected ListMenuElement, or None if the Menu has no element added to it.
        """
        if len(self.elements) > 0:
            return self.elements[self.selected_element_index]
        else:
            return None

    def select_next_element(self) -> Optional[ListMenuElement]:
        """
        Selects the next element of this menu's elements list
        :return: The resulting selected ListMenuElement, or None is the Menu has no element added to it
        """
        if not self.is_active:
            return self.get_selected_element()

        self.selected_element_index += 1
        if self.selected_element_index >= self.get_elements_count():
            self.selected_element_index = 0

        return self.get_selected_element()

    def select_previous_element(self) -> Optional[ListMenuElement]:
        """
        Selects the previous element of this menu's elements list
        :return: The resulting selected ListMenuElement, or None is the Menu has no element added to it
        """
        if not self.is_active:
            return self.get_selected_element()

        if len(self.elements) > 0:
            self.selected_element_index -= 1
            if self.selected_element_index < 0:
                self.selected_element_index = self.get_elements_count() - 1

        return self.get_selected_element()

    def activate_selected_element(self) -> None:
        """
        Activates the callback of the currently selected menu element
        :return: Nothing
        """
        element: ListMenuElement = self.get_selected_element()
        if element is not None:
            element.activate()

    def add_existing_element(self, new_element: ListMenuElement) -> None:
        """
        Adds an already created ListMenuElement to the current ListMenu
        :param new_element: The element to add to the current menu
        :return: Nothing
        """
        self.elements.append(new_element)

    def add_element(self, label: str, callback: Callable = None, *args, **kwargs) -> ListMenuElement:
        """
        Creates then adds a ListMenuElement to the current ListMenu
        :param label: The label that will appear for this element
        :param callback: The callback to assign to the new element
        :param args: Any args needed by your callback
        :param kwargs: Any kwargs needed by your callback
        :return:
        """
        new_element = ListMenuElement(label, callback, *args, **kwargs)
        self.add_existing_element(new_element)
        return new_element

    def draw(self) -> None:
        """
        Draws the menu on the console you specified at this menu instance's creation
        :return: Nothing
        """
        if self.is_hidden:
            return

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
        """
        Sets whether this menu is active or not
        Cannot change the selected element on inactive menus
        :param is_active: Is the menu active or not?
        :return: Nothing
        """
        self.is_active = is_active

    def set_hidden(self, is_hidden: bool) -> None:
        """
        Sets whether the menu should be hidden or not
        :param is_hidden: Is the menu hidden?
        :return: Nothing
        """
        self.is_hidden = is_hidden
