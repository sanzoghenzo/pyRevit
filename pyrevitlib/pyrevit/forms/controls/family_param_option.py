from .template_list_item import TemplateListItem


class FamilyParamOption(TemplateListItem):
    """Level wrapper for :func:`select_family_parameters`."""
    def __init__(self, fparam, builtin=False, labeled=False):
        super(FamilyParamOption, self).__init__(fparam)
        self.isbuiltin = builtin
        self.islabeled = labeled

    @property
    def name(self):
        """Family Parameter name."""
        return self.item.Definition.Name

    @property
    def istype(self):
        """Is type parameter."""
        return not self.item.IsInstance
