from pyrevit import HOST_APP
from pyrevit import PyRevitException
from pyrevit import UI
from pyrevit import coreutils
from pyrevit.forms.wpf_panel import WPFPanel


class _WPFPanelProvider(UI.IDockablePaneProvider):
    """Internal Panel provider for panels."""

    def __init__(self, panel_type, default_visible=True):
        self._panel_type = panel_type
        self._default_visible = default_visible
        self.panel = self._panel_type()

    def SetupDockablePane(self, data):
        """Setup forms.WPFPanel set on this instance."""
        # TODO: need to implement panel data
        # https://apidocs.co/apps/revit/2021.1/98157ec2-ab26-6ab7-2933-d1b4160ba2b8.htm
        data.FrameworkElement = self.panel
        data.VisibleByDefault = self._default_visible


def is_registered_dockable_panel(panel_type):
    """Check if dockable panel is already registered.

    Args:
        panel_type (forms.WPFPanel): dockable panel type
    """
    panel_uuid = coreutils.Guid.Parse(panel_type.panel_id)
    dockable_panel_id = UI.DockablePaneId(panel_uuid)
    return UI.DockablePane.PaneExists(dockable_panel_id)


def register_dockable_panel(panel_type, default_visible=True):
    """Register dockable panel.

    Args:
        panel_type (forms.WPFPanel): dockable panel type
        default_visible (bool, optional):
            whether panel should be visible by default
    """
    if not issubclass(panel_type, WPFPanel):
        raise PyRevitException(
            "Dockable pane must be a subclass of forms.WPFPanel"
            )

    panel_uuid = coreutils.Guid.Parse(panel_type.panel_id)
    dockable_panel_id = UI.DockablePaneId(panel_uuid)
    panel_provider = _WPFPanelProvider(panel_type, default_visible)
    HOST_APP.uiapp.RegisterDockablePane(
        dockable_panel_id,
        panel_type.panel_title,
        panel_provider
    )

    return panel_provider.panel


def open_dockable_panel(panel_type_or_id):
    """Open previously registered dockable panel.

    Args:
        panel_type_or_id (forms.WPFPanel, str): panel type or id
    """
    toggle_dockable_panel(panel_type_or_id, True)


def close_dockable_panel(panel_type_or_id):
    """Close previously registered dockable panel.

    Args:
        panel_type_or_id (forms.WPFPanel, str): panel type or id
    """
    toggle_dockable_panel(panel_type_or_id, False)


def toggle_dockable_panel(panel_type_or_id, state):
    """Toggle previously registered dockable panel.

    Args:
        panel_type_or_id (forms.WPFPanel | str): panel type or id
        state (bool): True to show the panel, False to hide it.
    """
    dpanel_id = None
    if isinstance(panel_type_or_id, str):
        panel_id = coreutils.Guid.Parse(panel_type_or_id)
        dpanel_id = UI.DockablePaneId(panel_id)
    elif issubclass(panel_type_or_id, WPFPanel):
        panel_id = coreutils.Guid.Parse(panel_type_or_id.panel_id)
        dpanel_id = UI.DockablePaneId(panel_id)
    else:
        raise PyRevitException("Given type is not a forms.WPFPanel")

    if dpanel_id:
        if UI.DockablePane.PaneIsRegistered(dpanel_id):
            dockable_panel = HOST_APP.uiapp.GetDockablePane(dpanel_id)
            if state:
                dockable_panel.Show()
            else:
                dockable_panel.Hide()
        else:
            raise PyRevitException(
                "Panel with id \"%s\" is not registered" % panel_type_or_id
                )
