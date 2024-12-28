import datetime

from .template_user_input_window import TemplateUserInputWindow


class GetValueWindow(TemplateUserInputWindow):
    """Standard form to get simple values from user.

    Examples:
        ```python
        from pyrevit import forms
        items = ['item1', 'item2', 'item3']
        forms.SelectFromList.show(items, button_name='Select Item')
        ['item1']
        ```
    """

    xaml_source = 'GetValueWindow.xaml'

    def _setup(self, **kwargs):
        self.Width = 400
        # determine value type
        self.value_type = kwargs.get('value_type', 'string')
        value_prompt = kwargs.get('prompt', None)
        value_default = kwargs.get('default', None)
        self.reserved_values = kwargs.get('reserved_values', [])

        # customize window based on type
        if self.value_type == 'string':
            self.show_element(self.stringPanel_dp)
            self.stringValue_tb.Text = value_default if value_default else ''
            self.stringValue_tb.Focus()
            self.stringValue_tb.SelectAll()
            self.stringPrompt.Text = value_prompt if value_prompt else 'Enter string:'
            if self.reserved_values:
                self.string_value_changed(None, None)
        elif self.value_type == 'dropdown':
            self.show_element(self.dropdownPanel_db)
            self.dropdownPrompt.Text = value_prompt if value_prompt else 'Pick one value:'
            self.dropdown_cb.ItemsSource = self._context
            if value_default:
                self.dropdown_cb.SelectedItem = value_default
        elif self.value_type == 'date':
            self.show_element(self.datePanel_dp)
            self.datePrompt.Text = value_prompt if value_prompt else 'Pick date:'
        elif self.value_type == 'slider':
            self.show_element(self.sliderPanel_sp)
            self.sliderPrompt.Text = value_prompt
            self.numberPicker.Minimum = kwargs.get('min', 0)
            self.numberPicker.Maximum = kwargs.get('max', 100)
            self.numberPicker.TickFrequency = kwargs.get('interval', 1)
            self.numberPicker.Value = (
                value_default if isinstance(value_default, (float, int))
                else self.numberPicker.Minimum
            )

    def string_value_changed(self, _sender, _args):
        """Handle string vlaue update event."""
        filtered_rvalues = sorted(
            [x for x in self.reserved_values if self.stringValue_tb.Text == str(x)]
        )
        similar_rvalues = sorted(
            [x for x in self.reserved_values if self.stringValue_tb.Text in str(x)],
            reverse=True
        )
        filtered_rvalues.extend(similar_rvalues)
        if filtered_rvalues:
            self.reservedValuesList.ItemsSource = filtered_rvalues
            self.show_element(self.reservedValuesListPanel)
            self.okayButton.IsEnabled = self.stringValue_tb.Text not in filtered_rvalues
        else:
            self.reservedValuesList.ItemsSource = []
            self.hide_element(self.reservedValuesListPanel)
            self.okayButton.IsEnabled = True

    def select(self, _sender, _args):
        """Process input data and set the response."""
        self.Close()
        if self.value_type == 'string':
            self.response = self.stringValue_tb.Text
        elif self.value_type == 'dropdown':
            self.response = self.dropdown_cb.SelectedItem
        elif self.value_type == 'date':
            if self.datePicker.SelectedDate:
                datestr = self.datePicker.SelectedDate.ToString("MM/dd/yyyy")
                self.response = datetime.datetime.strptime(datestr, r'%m/%d/%Y')
            else:
                self.response = None
        elif self.value_type == 'slider':
            self.response = self.numberPicker.Value
