"""Mixin class for WPF property updater."""
import pyevent

from pyrevit.framework import ComponentModel


class Reactive(ComponentModel.INotifyPropertyChanged):
    """WPF property updater base mixin."""
    PropertyChanged, _propertyChangedCaller = pyevent.make_event()

    def add_PropertyChanged(self, value):
        """Called when a property is added to the object."""
        self.PropertyChanged += value

    def remove_PropertyChanged(self, value):
        """Called when a property is removed from the object."""
        self.PropertyChanged -= value

    def OnPropertyChanged(self, prop_name):
        """Called when a property is changed.

        Args:
            prop_name (str): property name
        """
        if self._propertyChangedCaller:
            args = ComponentModel.PropertyChangedEventArgs(prop_name)
            self._propertyChangedCaller(self, args)
