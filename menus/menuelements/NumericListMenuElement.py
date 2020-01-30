from typing import Union


class NumericListMenuElement:
    """
    A menu element to which you can attach an integer or float value.
    On activation, the user will be able to modify the value of the element.
    """
    def __init__(self, label: str, initial_value: Union[int, float]):
        self.label = label
        self.value: Union[int, float] = initial_value
