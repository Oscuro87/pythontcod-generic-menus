from tcod.console import Console
from typing import List, Callable, Optional, Union
import config as CFG
from menus.menuelements.CallbackListMenuElement import CallbackListMenuElement
from menus.menuelements.ListMenuElementEnum import ListMenuElementEnum
from menus.menuelements.ListMenuElementFactory import ListMenuElementFactory
from menus.menuelements.NumericListMenuElement import NumericListMenuElement
from .MenuBase import MenuBase


ListMenuAcceptedElement = Union[CallbackListMenuElement, NumericListMenuElement]
ListMenuAcceptedElementsList = List[Union[CallbackListMenuElement, NumericListMenuElement]]


class ListMenu(MenuBase):
    """
    A simple list menu with no special elements, just plain straight elements.
    Each element can be assigned a callback (to which you can pass parameters through *args / **kwargs),
        to interact with you app.
    """

    def __init__(self, console: Console = None, start_active: bool = True, start_hidden: bool = False):
        """
        Creates a new ListMenu
        :param console: The TCOD Console you wish to draw the menu upon. It can be the root console, as well
            as a console that you blit on the root console afterwards.
        """
        super().__init__(console, start_active, start_hidden)
        self.selected_element_index = 0
        self.elements: ListMenuAcceptedElementsList = []

    def get_elements_count(self) -> int:
        return len(self.elements)

    def get_selected_element(self) -> Optional[ListMenuAcceptedElement]:
        """
        Gets the currently selected element of this menu
        :return: The selected ListMenuElement, or None if the Menu has no element added to it.
        """
        if len(self.elements) > 0:
            return self.elements[self.selected_element_index]
        else:
            return None

    def select_next_element(self) -> Optional[ListMenuAcceptedElement]:
        """
        Selects the next element of this menu's elements list
        :return: The resulting selected ListMenuElement, or None is the Menu has no element added to it
        """
        if not self.is_active():
            return self.get_selected_element()

        self.selected_element_index += 1
        if self.selected_element_index >= self.get_elements_count():
            self.selected_element_index = 0

        return self.get_selected_element()

    def select_previous_element(self) -> Optional[ListMenuAcceptedElement]:
        """
        Selects the previous element of this menu's elements list
        :return: The resulting selected ListMenuElement, or None is the Menu has no element added to it
        """
        if not self.is_active():
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
        element: ListMenuAcceptedElement = self.get_selected_element()
        if element is not None:
            element.activate()

    def add_existing_element(self, new_element: ListMenuAcceptedElement) -> None:
        """
        Adds an already created ListMenuElement to the current ListMenu
        :param new_element: The element to add to the current menu
        :return: Nothing
        """
        self.elements.append(new_element)

    def create_and_add_element(self, element_type: ListMenuElementEnum, label, *args, **kwargs) -> None:
        """
        Creates (using the List Menu Elements Factory) and adds the product of the factory to the current ListMenu
        :param element_type: The type of element to add, see ListMenuElementEnum for a list of available element types
        :param label: The label of the new element, common to all element types
        :param args: The additional args to pass to the factory
        :param kwargs: The additional kwargs to pass to the factory
        :return: None
        """
        new_element = ListMenuElementFactory.create_list_menu_element(element_type, label, *args, *kwargs)
        self.add_existing_element(new_element)

    def draw(self) -> None:
        """
        Draws the menu on the console you specified at this menu instance's creation
        :return: Nothing
        """
        super(ListMenu, self).draw()

        if self.is_hidden() or self.console is None:
            return

        if self.console.width < CFG.DRAW__MINIMUM_CONSOLE_WIDTH and CFG.DEBUG_MODE:
            raise RuntimeWarning('Warning: minimum console width to draw menu is not met!')
        if self.console.height < self.get_elements_count() and CFG.DEBUG_MODE:
            raise RuntimeWarning('Warning: Console height cannot fit all elements (TODO: scrolling)')

        count = 0
        element: ListMenuAcceptedElement
        currently_selected: ListMenuAcceptedElement = self.get_selected_element()
        for element in self.elements:
            if element == currently_selected:
                self.console.print(0, count, element.label, (0, 0, 0), (255, 255, 255))
            else:
                self.console.print(0, count, element.label)
            count += 1
