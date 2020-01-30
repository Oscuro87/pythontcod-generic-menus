from tcod.console import Console


class MenuBase:
    """
    This is a base menu from which other menus will derive from.
    It is not useable "as is".
    """
    def __init__(self, console: Console, start_active: bool, start_hidden: bool):
        self.console = console
        self.active = start_active
        self.hidden = start_hidden

    def set_active(self, is_active: bool) -> None:
        """
        Sets whether this menu is active or not
        Cannot change the selected element on inactive menus
        :param is_active: Is the menu active or not?
        :return: Nothing
        """
        self.active = is_active

    def is_active(self) -> bool:
        return self.active

    def set_hidden(self, is_hidden: bool) -> None:
        """
        Sets whether the menu should be hidden or not
        :param is_hidden: Is the menu hidden?
        :return: Nothing
        """
        self.hidden = is_hidden

    def is_hidden(self) -> bool:
        return self.hidden

    def draw(self) -> None:
        pass

    def set_console(self, new_console: Console) -> None:
        self.console = new_console

    def get_console(self) -> Console:
        return self.console
