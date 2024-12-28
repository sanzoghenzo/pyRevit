from pyrevit import DB

from .template_list_item import TemplateListItem


class RevisionOption(TemplateListItem):
    """Revision wrapper for :func:`select_revisions`."""
    def __init__(self, revision_element):
        super(RevisionOption, self).__init__(revision_element)

    @property
    def name(self):
        """Revision name (description)."""
        rev_settings = DB.RevisionSettings.GetRevisionSettings(self.item.Document)
        if rev_settings.RevisionNumbering == DB.RevisionNumbering.PerProject:
            revnum = self.item.RevisionNumber
        else:
            revnum = self.item.SequenceNumber
        return '{}-{}-{}'.format(revnum, self.item.Description, self.item.RevisionDate)
