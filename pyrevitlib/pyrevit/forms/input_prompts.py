from pyrevit.framework import Forms
from pyrevit.framework import System
from .get_value_window import GetValueWindow
from .alerts import alert


def ask_for_string(default=None, prompt=None, title=None, **kwargs):
    """Ask user to select a string value.

    This is a shortcut function that configures :obj:`GetValueWindow` for
    string data types. kwargs can be used to pass on other arguments.

    Args:
        default (str): default unique string. must not be in reserved_values
        prompt (str): prompt message
        title (str): title message
        kwargs (type): other arguments to be passed to :obj:`GetValueWindow`

    Returns:
        (str): selected string value

    Examples:
        ```python
        forms.ask_for_string(
            default='some-tag',
            prompt='Enter new tag name:',
            title='Tag Manager')
        'new-tag'
        ```
    """
    return GetValueWindow.show(
        None, value_type='string', default=default, prompt=prompt, title=title, **kwargs
    )


def ask_for_unique_string(
    reserved_values, default=None, prompt=None, title=None, **kwargs
):
    """Ask user to select a unique string value.

    This is a shortcut function that configures :obj:`GetValueWindow` for
    unique string data types. kwargs can be used to pass on other arguments.

    Args:
        reserved_values (list[str]): list of reserved (forbidden) values
        default (str): default unique string. must not be in reserved_values
        prompt (str): prompt message
        title (str): title message
        kwargs (type): other arguments to be passed to :obj:`GetValueWindow`

    Returns:
        (str): selected unique string

    Examples:
        ```python
        forms.ask_for_unique_string(
            prompt='Enter a Unique Name',
            title=self.Title,
            reserved_values=['Ehsan', 'Gui', 'Guido'],
            owner=self)
        'unique string'
        ```

        In example above, owner argument is provided to be passed to underlying
        :obj:`GetValueWindow`.

    """
    return GetValueWindow.show(
        None,
        value_type='string',
        default=default,
        prompt=prompt,
        title=title,
        reserved_values=reserved_values,
        **kwargs,
    )


def ask_for_one_item(items, default=None, prompt=None, title=None, **kwargs):
    """Ask user to select an item from a list of items.

    This is a shortcut function that configures :obj:`GetValueWindow` for
    'single-select' data types. kwargs can be used to pass on other arguments.

    Args:
        items (list[str]): list of items to choose from
        default (str): default selected item
        prompt (str): prompt message
        title (str): title message
        kwargs (type): other arguments to be passed to :obj:`GetValueWindow`

    Returns:
        (str): selected item

    Examples:
        ```python
        forms.ask_for_one_item(
            ['test item 1', 'test item 2', 'test item 3'],
            default='test item 2',
            prompt='test prompt',
            title='test title'
        )
        'test item 1'
        ```
    """
    return GetValueWindow.show(
        items,
        value_type='dropdown',
        default=default,
        prompt=prompt,
        title=title,
        **kwargs,
    )


def ask_for_date(default=None, prompt=None, title=None, **kwargs):
    """Ask user to select a date value.

    This is a shortcut function that configures :obj:`GetValueWindow` for
    date data types. kwargs can be used to pass on other arguments.

    Args:
        default (datetime.datetime): default selected date value
        prompt (str): prompt message
        title (str): title message
        kwargs (type): other arguments to be passed to :obj:`GetValueWindow`

    Returns:
        (datetime.datetime): selected date

    Examples:
        ```python
        forms.ask_for_date(default="", title="Enter deadline:")
        datetime.datetime(2019, 5, 17, 0, 0)
        ```
    """
    # FIXME: window does not set default value
    return GetValueWindow.show(
        None,
        value_type='date',
        default=default,
        prompt=prompt,
        title=title,
        **kwargs,
    )


def ask_for_number_slider(
    default=None, min=0, max=100, interval=1, prompt=None, title=None, **kwargs
):
    """Ask user to select a number value.

    This is a shortcut function that configures :obj:`GetValueWindow` for
    numbers. kwargs can be used to pass on other arguments.

    Args:
        default (str): default unique string. must not be in reserved_values
        min (int): minimum value on slider
        max (int): maximum value on slider
        interval (int): number interval between values
        prompt (str): prompt message
        title (str): title message
        kwargs (type): other arguments to be passed to :obj:`GetValueWindow`

    Returns:
        (str): selected string value

    Examples:
        ```python
        forms.ask_for_number_slider(
            default=50,
            min = 0,
            max = 100,
            interval = 5,
            prompt='Select a number:',
            title='test title')
        '50'
        ```
    
    In this example, the slider will allow values such as '40, 45, 50, 55, 60' etc
    """
    return GetValueWindow.show(
        None,
        value_type='slider',
        default=default,
        prompt=prompt,
        title=title,
        max=max,
        min=min,
        interval=interval,
        **kwargs,
    )


def ask_to_use_selected(type_name, count=None, multiple=True):
    """Ask user if wants to use currently selected elements.

    Args:
        type_name (str): Element type of expected selected elements
        count (int): Number of selected items
        multiple (bool): Whether multiple selected items are allowed
    """
    report = type_name.lower()
    # multiple = True
    message = \
        "You currently have %s selected. Do you want to proceed with "\
        "currently selected item(s)?"
    # check is selecting multiple is allowd
    if not multiple:
        # multiple = False
        message = \
            "You currently have %s selected and only one is required. "\
            "Do you want to use the first selected item?"

    # check if count is provided
    if count is not None:
        report = '{} {}'.format(count, report)
    return alert(message % report, yes=True, no=True)


def ask_for_color(default=None):
    """Show system color picker and ask for color.

    Args:
        default (str): default color in HEX ARGB e.g. #ff808080

    Returns:
        (str): selected color in HEX ARGB e.g. #ff808080, or None if cancelled

    Examples:
        ```python
        forms.ask_for_color()
        '#ff808080'
        ```
    """
    # colorDlg.Color
    color_picker = Forms.ColorDialog()
    if default:
        default = default.replace('#', '')
        color_picker.Color = System.Drawing.Color.FromArgb(
            int(default[:2], 16),
            int(default[2:4], 16),
            int(default[4:6], 16),
            int(default[6:8], 16)
        )
    color_picker.FullOpen = True
    if color_picker.ShowDialog() == Forms.DialogResult.OK:
        c = color_picker.Color
        c_hex = ''.join('{:02X}'.format(int(x)) for x in [c.A, c.R, c.G, c.B])
        return '#' + c_hex
