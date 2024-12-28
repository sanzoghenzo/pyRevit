import os
import os.path as op
import webbrowser

from pyrevit import EXEC_PARAMS
from pyrevit import PyRevitException
from pyrevit.forms.wpf_window import WPFWindow
from pyrevit.framework import Windows
from pyrevit.framework import get_current_thread_id
from pyrevit.framework import wpf


class WPFPanel(Windows.Controls.Page):
    r"""WPF panel base class for all pyRevit dockable panels.

    panel_id (str) must be set on the type to dockable panel uuid
    panel_source (str): xaml source filepath

    Examples:
        ```python
        from pyrevit import forms
        class MyPanel(forms.WPFPanel):
            panel_id = "181e05a4-28f6-4311-8a9f-d2aa528c8755"
            panel_source = "MyPanel.xaml"

        forms.register_dockable_panel(MyPanel)
        # then from the button that needs to open the panel
        forms.open_dockable_panel("181e05a4-28f6-4311-8a9f-d2aa528c8755")
        ```
    """

    panel_id = None
    panel_source = None

    def __init__(self):
        """Initialize WPF panel and resources."""
        if not self.panel_id:
            raise PyRevitException("\"panel_id\" property is not set")
        if not self.panel_source:
            raise PyRevitException("\"panel_source\" property is not set")

        if not op.exists(self.panel_source):
            wpf.LoadComponent(
                self, os.path.join(EXEC_PARAMS.command_path, self.panel_source)
            )
        else:
            wpf.LoadComponent(self, self.panel_source)

        # set properties
        self.thread_id = get_current_thread_id()
        WPFWindow.setup_resources(self)

    def set_image_source(self, wpf_element, image_file):
        """Set source file for image element.

        Args:
            wpf_element (System.Windows.Controls.Image): xaml image element
            image_file (str): image file path
        """
        WPFWindow.set_image_source_file(wpf_element, image_file)

    @staticmethod
    def hide_element(*wpf_elements):
        """Collapse elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be collaped
        """
        WPFPanel.hide_element(*wpf_elements)

    @staticmethod
    def show_element(*wpf_elements):
        """Show collapsed elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be set to visible.
        """
        WPFPanel.show_element(*wpf_elements)

    @staticmethod
    def toggle_element(*wpf_elements):
        """Toggle visibility of elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be toggled.
        """
        WPFPanel.toggle_element(*wpf_elements)

    @staticmethod
    def disable_element(*wpf_elements):
        """Enable elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be enabled
        """
        WPFPanel.disable_element(*wpf_elements)

    @staticmethod
    def enable_element(*wpf_elements):
        """Enable elements.

        Args:
            *wpf_elements (list): WPF framework elements to be enabled
        """
        WPFPanel.enable_element(*wpf_elements)

    def handle_url_click(self, sender, _args):
        """Callback for handling click on package website url."""
        return webbrowser.open_new_tab(sender.NavigateUri.AbsoluteUri)
