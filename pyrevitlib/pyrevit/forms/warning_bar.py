from .template_prompt_bar import TemplatePromptBar


class WarningBar(TemplatePromptBar):
    """Show warning bar at the top of Revit window.

    Keyword Args:
        title (string): warning bar text

    Examples:
        ```python
        with WarningBar(title='my warning'):
           # do stuff
        ```
    """

    xaml_source = 'WarningBar.xaml'

    def _setup(self, **kwargs):
        self.message_tb.Text = kwargs.get('title', '')
