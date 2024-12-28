from pyrevit.revit.db.query import get_name

from .template_list_item import TemplateListItem


class ViewOption(TemplateListItem):
    """View wrapper for :func:`select_views`."""

    @property
    def name(self):
        """View name."""
        return '{} ({})'.format(get_name(self.item), self.item.ViewType)
