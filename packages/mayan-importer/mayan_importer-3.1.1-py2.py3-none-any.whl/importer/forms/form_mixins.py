from django import forms as django_forms


class FormMixinState:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['state'].initial = self.instance._meta.state_default
        self.fields['state'].required = False
        self.fields['state'].widget = django_forms.Select(
            attrs={'class': 'select2'},
            choices=self.instance._meta.state_choices
        )
