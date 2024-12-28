"""Context manager to toggle window visibility."""

class WindowToggler(object):
    """Context manager to toggle window visibility."""
    def __init__(self, window):
        self._window = window

    def __enter__(self):
        self._window.hide()

    def __exit__(self, exception, exception_value, traceback):
        self._window.show_dialog()
