import os.path as op

from pyrevit.framework import Windows
from pyrevit.forms.constants import DEFAULT_INPUTWINDOW_WIDTH
from pyrevit.forms.constants import DEFAULT_INPUTWINDOW_HEIGHT
from .wpf_window import WPFWindow


class TemplateUserInputWindow(WPFWindow):
    """Base class for pyRevit user input standard forms.

    Args:
        context (any): window context element(s)
        title (str): window title
        width (int): window width
        height (int): window height
        **kwargs (Any): other arguments to be passed to :func:`_setup`
    """

    xaml_source = 'BaseWindow.xaml'

    def __init__(self, context, title, width, height, **kwargs):
        """Initialize user input window."""
        super(TemplateUserInputWindow, self).__init__(
            op.join(op.dirname(__file__), self.xaml_source), handle_esc=True
        )
        self.Title = title or 'pyRevit'
        self.Width = width
        self.Height = height

        self._context = context
        self.response = None

        # parent window?
        owner = kwargs.get('owner', None)
        if owner:
            # set wpf windows directly
            self.Owner = owner
            self.WindowStartupLocation = Windows.WindowStartupLocation.CenterOwner

        self._setup(**kwargs)

    def _setup(self, **kwargs):
        """Private method to be overriden by subclasses for window setup."""
        pass

    @classmethod
    def show(
        cls,
        context,
        title='User Input',
        width=DEFAULT_INPUTWINDOW_WIDTH,
        height=DEFAULT_INPUTWINDOW_HEIGHT,
        **kwargs
    ):
        """Show user input window.

        Args:
            context (any): window context element(s)
            title (str): window title
            width (int): window width
            height (int): window height
            **kwargs (any): other arguments to be passed to window
        """
        dlg = cls(context, title, width, height, **kwargs)
        dlg.ShowDialog()
        return dlg.response
