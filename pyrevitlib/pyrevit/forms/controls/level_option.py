from pyrevit.revit.db.query import get_name

from .template_list_item import TemplateListItem

class LevelOption(TemplateListItem):
    """Level wrapper for :func:`select_levels`."""
    @property
    def name(self):
        """Level name."""
        return get_name(self.item)
