from .template_list_item import TemplateListItem


class SheetOption(TemplateListItem):
    """Sheet wrapper for :func:`select_sheets`."""
    def __init__(self, sheet_element):
        super(SheetOption, self).__init__(sheet_element)

    @property
    def name(self):
        """Sheet name."""
        placeholder = ' (placeholder)' if self.item.IsPlaceholder else ''
        return '{} - {}{}'.format(self.item.SheetNumber, self.item.Name, placeholder)

    @property
    def number(self):
        """Sheet number."""
        return self.item.SheetNumber
