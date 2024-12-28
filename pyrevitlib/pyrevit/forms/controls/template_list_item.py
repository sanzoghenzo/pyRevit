from pyrevit.compat import safe_strtype
from pyrevit.forms.constants import WPF_VISIBLE
from pyrevit.forms.constants import WPF_COLLAPSED
from .reactive import Reactive
from .reactive_property import reactive


class TemplateListItem(Reactive):
    """Base class for checkbox option wrapping another object."""

    def __init__(self, orig_item, checked=False, checkable=True, name_attr=None):
        """Initialize the checkbox option and wrap given obj.

        Args:
            orig_item (any): Object to wrap (must have name property
                             or be convertable to string with str()
            checked (bool): Initial state. Defaults to False
            checkable (bool): Use checkbox for items
            name_attr (str): Get this attribute of wrapped object as name
        """
        super(TemplateListItem, self).__init__()
        self.item = orig_item
        self.state = checked
        self._nameattr = name_attr
        self._checkable = checkable

    def __nonzero__(self):
        return self.state

    def __str__(self):
        return self.name or str(self.item)

    def __contains__(self, value):
        return value in self.name

    def __getattr__(self, param_name):
        return getattr(self.item, param_name)

    @property
    def name(self):
        """Name property."""
        # get custom attr, or name or just str repr
        if self._nameattr:
            return safe_strtype(getattr(self.item, self._nameattr))
        elif hasattr(self.item, 'name'):
            return getattr(self.item, 'name', '')
        else:
            return safe_strtype(self.item)

    def unwrap(self):
        """Unwrap and return wrapped object."""
        return self.item

    @reactive
    def checked(self):
        """Id checked."""
        return self.state

    @checked.setter
    def checked(self, value):
        self.state = value

    @property
    def checkable(self):
        """List Item CheckBox Visibility."""
        return WPF_VISIBLE if self._checkable else WPF_COLLAPSED

    @checkable.setter
    def checkable(self, value):
        self._checkable = value
