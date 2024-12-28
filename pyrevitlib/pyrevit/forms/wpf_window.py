import os
import os.path
import threading
import webbrowser

from pyrevit import BIN_DIR
from pyrevit import EXEC_PARAMS
from pyrevit import coreutils
from pyrevit import framework
from pyrevit import versionmgr
from pyrevit.api import AdWindows
from pyrevit.forms import utils
from pyrevit.forms.constants import DEFAULT_RECOGNIZE_ACCESS_KEY
from pyrevit.forms.constants import WPF_COLLAPSED
from pyrevit.forms.constants import WPF_VISIBLE
from pyrevit.forms.window_toggler import WindowToggler
from pyrevit.framework import Input
from pyrevit.framework import Interop
from pyrevit.framework import Media
from pyrevit.framework import Uri
from pyrevit.framework import UriKind
from pyrevit.framework import ResourceDictionary
from pyrevit.framework import System
from pyrevit.framework import Threading
from pyrevit.framework import wpf
from pyrevit.userconfig import user_config

class WPFWindow(framework.Windows.Window):
    r"""WPF Window base class for all pyRevit forms.

    Args:
        xaml_source (str): xaml source filepath or xaml content
        literal_string (bool): xaml_source contains xaml content, not filepath
        handle_esc (bool): handle Escape button and close the window
        set_owner (bool): set the owner of window to host app window

    Examples:
        ```python
        from pyrevit import forms
        layout = '<Window ' \
                 'xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" ' \
                 'xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml" ' \
                 'ShowInTaskbar="False" ResizeMode="NoResize" ' \
                 'WindowStartupLocation="CenterScreen" ' \
                 'HorizontalContentAlignment="Center">' \
                 '</Window>'
        w = forms.WPFWindow(layout, literal_string=True)
        w.show()
        ```
    """

    def __init__(self, xaml_source, literal_string=False, handle_esc=True, set_owner=True):
        """Initialize WPF window and resources."""
        self.load_xaml(
            xaml_source,
            literal_string=literal_string,
            handle_esc=handle_esc,
            set_owner=set_owner
        )

    def load_xaml(self, xaml_source, literal_string=False, handle_esc=True, set_owner=True):
        """Load the window XAML file.

        Args:
            xaml_source (str): The XAML content or file path to load.
            literal_string (bool, optional): True if `xaml_source` is content,
                False if it is a path. Defaults to False.
            handle_esc (bool, optional): Whether the ESC key should be handled.
                Defaults to True.
            set_owner (bool, optional): Whether to se the window owner.
                Defaults to True.
        """
        # create new id for this window
        self.window_id = coreutils.new_uuid()

        if not literal_string:
            wpf.LoadComponent(self, self._determine_xaml(xaml_source))
        else:
            wpf.LoadComponent(self, framework.StringReader(xaml_source))

        # set properties
        self.thread_id = framework.get_current_thread_id()
        if set_owner:
            self.setup_owner()
        self.setup_icon()
        WPFWindow.setup_resources(self)
        if handle_esc:
            self.setup_default_handlers()


    def _determine_xaml(self, xaml_source):
        xaml_file = xaml_source
        if not os.path.exists(xaml_file):
            xaml_file = os.path.join(EXEC_PARAMS.command_path, xaml_source)

        english_xaml_file = xaml_file.replace('.xaml', '.en_us.xaml')
        localized_xaml_file = xaml_file.replace(
            '.xaml',
            '.{}.xaml'.format(user_config.user_locale)
        )

        english_xaml_resfile = xaml_file.replace(
            '.xaml', '.ResourceDictionary.en_us.xaml'
        )
        localized_xaml_resfile = xaml_file.replace(
            '.xaml',
            '.ResourceDictionary.{}.xaml'.format(user_config.user_locale)
        )

        # if localized version of xaml file is provided, use that
        if os.path.isfile(localized_xaml_file):
            return localized_xaml_file

        if os.path.isfile(english_xaml_file):
            return english_xaml_file

        # otherwise look for .ResourceDictionary files and load those,
        # returning the original xaml_file
        if os.path.isfile(localized_xaml_resfile):
            self.merge_resource_dict(localized_xaml_resfile)

        elif os.path.isfile(english_xaml_resfile):
            self.merge_resource_dict(english_xaml_resfile)

        return xaml_file

    def merge_resource_dict(self, xaml_source):
        """Merge a ResourceDictionary xaml file with this window.

        Args:
            xaml_source (str): xaml file with the resource dictionary
        """
        lang_dictionary = ResourceDictionary()
        lang_dictionary.Source = Uri(xaml_source, UriKind.Absolute)
        self.Resources.MergedDictionaries.Add(lang_dictionary)

    def get_locale_string(self, string_name):
        """Get localized string.

        Args:
            string_name (str): string name

        Returns:
            (str): localized string
        """
        return self.FindResource(string_name)

    def setup_owner(self):
        """Set the window owner."""
        wih = Interop.WindowInteropHelper(self)
        wih.Owner = AdWindows.ComponentManager.ApplicationWindow

    @staticmethod
    def setup_resources(wpf_ctrl):
        """Sets the WPF resources."""
        #f39c12
        accent_color = Media.Color.FromArgb(0xFF, 0xf3, 0x9c, 0x12)
        #2c3e50
        dark_color = Media.Color.FromArgb(0xFF, 0x2c, 0x3e, 0x50)
        #23303d
        darker_color = Media.Color.FromArgb(0xFF, 0x23, 0x30, 0x3d)
        #ffffff
        button_color = Media.Color.FromArgb(0xFF, 0xff, 0xff, 0xff)
        wpf_ctrl.Resources['pyRevitDarkColor'] = dark_color
        wpf_ctrl.Resources['pyRevitDarkerDarkColor'] = darker_color
        wpf_ctrl.Resources['pyRevitButtonColor'] = button_color
        wpf_ctrl.Resources['pyRevitAccentColor'] = accent_color
        wpf_ctrl.Resources['pyRevitDarkBrush'] = Media.SolidColorBrush(dark_color)
        wpf_ctrl.Resources['pyRevitAccentBrush'] = Media.SolidColorBrush(accent_color)
        wpf_ctrl.Resources['pyRevitDarkerDarkBrush'] = Media.SolidColorBrush(darker_color)
        wpf_ctrl.Resources['pyRevitButtonForgroundBrush'] = Media.SolidColorBrush(button_color)
        wpf_ctrl.Resources['pyRevitRecognizesAccessKey'] = DEFAULT_RECOGNIZE_ACCESS_KEY

    def setup_default_handlers(self):
        """Set the default handlers."""
        self.PreviewKeyDown += self.handle_input_key

    def handle_input_key(self, _sender, args):
        """Handle keyboard input and close the window on Escape."""
        if args.Key == Input.Key.Escape:
            self.Close()

    def set_icon(self, icon_path):
        """Set window icon to given icon path."""
        self.Icon = utils.bitmap_from_file(icon_path)

    def setup_icon(self):
        """Setup default window icon."""
        self.set_icon(os.path.join(BIN_DIR, 'pyrevit_settings.png'))

    def hide(self):
        """Hide window."""
        self.Hide()

    def show(self, modal=False):
        """Show window."""
        if modal:
            return self.ShowDialog()
        # else open non-modal
        self.Show()

    def show_dialog(self):
        """Show modal window."""
        return self.ShowDialog()

    @staticmethod
    def set_image_source_file(wpf_element, image_file):
        """Set source file for image element.

        Args:
            wpf_element (System.Windows.Controls.Image): xaml image element
            image_file (str): image file path
        """
        if not os.path.exists(image_file):
            wpf_element.Source = \
                utils.bitmap_from_file(
                    os.path.join(EXEC_PARAMS.command_path,
                                 image_file)
                    )
        else:
            wpf_element.Source = utils.bitmap_from_file(image_file)

    def set_image_source(self, wpf_element, image_file):
        """Set source file for image element.

        Args:
            wpf_element (System.Windows.Controls.Image): xaml image element
            image_file (str): image file path
        """
        WPFWindow.set_image_source_file(wpf_element, image_file)

    def dispatch(self, func, *args, **kwargs):
        """Runs the function in a new thread.

        Args:
            func (Callable): function to run
            *args (Any): positional arguments to pass to func
            **kwargs (Any): keyword arguments to pass to func
        """
        if framework.get_current_thread_id() == self.thread_id:
            t = threading.Thread(
                target=func,
                args=args,
                kwargs=kwargs
                )
            t.start()
        else:
            # ask ui thread to call the func with args and kwargs
            self.Dispatcher.Invoke(
                System.Action(lambda: func(*args, **kwargs)),
                Threading.DispatcherPriority.Background
            )

    def conceal(self):
        """Conceal window."""
        return WindowToggler(self)

    @property
    def pyrevit_version(self):
        """Active pyRevit formatted version e.g. '4.9-beta'."""
        return 'pyRevit {}'.format(versionmgr.get_pyrevit_version().get_formatted())

    @staticmethod
    def hide_element(*wpf_elements):
        """Collapse elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be collaped
        """
        for wpfel in wpf_elements:
            wpfel.Visibility = WPF_COLLAPSED

    @staticmethod
    def show_element(*wpf_elements):
        """Show collapsed elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be set to visible.
        """
        for wpfel in wpf_elements:
            wpfel.Visibility = WPF_VISIBLE

    @staticmethod
    def toggle_element(*wpf_elements):
        """Toggle visibility of elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be toggled.
        """
        for wpfel in wpf_elements:
            if wpfel.Visibility == WPF_VISIBLE:
                WPFWindow.hide_element(wpfel)
            elif wpfel.Visibility == WPF_COLLAPSED:
                WPFWindow.show_element(wpfel)

    @staticmethod
    def disable_element(*wpf_elements):
        """Enable elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be enabled
        """
        for wpfel in wpf_elements:
            wpfel.IsEnabled = False

    @staticmethod
    def enable_element(*wpf_elements):
        """Enable elements.

        Args:
            *wpf_elements (list[UIElement]): WPF framework elements to be enabled
        """
        for wpfel in wpf_elements:
            wpfel.IsEnabled = True

    def handle_url_click(self, sender, _args):
        """Callback for handling click on package website url."""
        return webbrowser.open_new_tab(sender.NavigateUri.AbsoluteUri)
