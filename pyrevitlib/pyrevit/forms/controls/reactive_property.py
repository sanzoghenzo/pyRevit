"""Property decorator for WPF bound properties.

https://gui-at.blogspot.com/2009/11/inotifypropertychanged-in-ironpython.html
"""

class reactive(property):
    """Decorator for WPF bound properties."""

    def __init__(self, getter):
        def newgetter(ui_control):
            try:
                return getter(ui_control)
            except AttributeError:
                return None

        super(reactive, self).__init__(newgetter)

    def setter(self, setter):
        """Property setter."""
        def newsetter(ui_control, newvalue):
            oldvalue = self.fget(ui_control)
            if oldvalue != newvalue:
                setter(ui_control, newvalue)
                ui_control.OnPropertyChanged(setter.__name__)

        return property(
            fget=self.fget,
            fset=newsetter,
            fdel=self.fdel,
            doc=self.__doc__,
        )
