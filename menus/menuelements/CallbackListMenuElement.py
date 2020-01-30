from typing import Callable
import config as CFG


class CallbackListMenuElement:
    """
    A simple menu element that triggers a callback on activation.
    The element accepts a label (required), and a callback (required)
    """

    def __init__(self, label: str, callback: Callable, *args, **kwargs):
        self.label = label
        self.cb = callback if callback is not None else self.default_activation_handler
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

    def default_activation_handler(self, *args, **kwargs) -> None:
        """
        Don't mind this, it was just for testing purpose
        """
        # if CFG.DEBUG_MODE:
        print("Default callback called for menu element with label {}".format(self.label))

    def set_callback(self, fn: Callable) -> "CallbackListMenuElement":
        """
        Chain-friendly method; sets a callback to the current instance
        :param fn: The callback to assign to this instance
        :return: Returns self, to allow chaining methods
        """
        self.cb = fn
        return self

    def set_cb(self, fn: Callable) -> "CallbackListMenuElement":
        """
        Just an alias for the set_callback method, see above!
        """
        return self.set_callback(fn)

    def set_args(self, args) -> "CallbackListMenuElement":
        """
        Sets the args, read by the callback when it is activated.
        Args are not required, unless needed by your callback implementation.
        :param args: The args to assign to the current instance
        :return: Returns self, to allow chaining methods
        """
        self.args = args
        return self

    def set_kwargs(self, kwargs) -> "CallbackListMenuElement":
        """
        Sets the kwargs, read by the callback when it is activated.
        Kwargs are not required, unless needed by your callback implementation.
        :param kwargs: The kwargs to assign to the current instance
        :return: Returns self, to allow chaining methods
        """
        self.kwargs = kwargs
        return self
