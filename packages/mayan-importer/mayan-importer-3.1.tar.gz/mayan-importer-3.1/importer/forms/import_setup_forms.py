from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.backends.forms import FormDynamicModelBackend
from mayan.apps.views import forms

from ..classes import ImportSetupBackend
from ..models import ImportSetup

from .form_mixins import FormMixinState


class ImportSetupBackendSelectionForm(forms.Form):
    backend = django_forms.ChoiceField(
        choices=(), label=_(message='Backend'), help_text=_(
            message='The backend to use for the import setup.'
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['backend'].choices = ImportSetupBackend.get_choices()


class ImportSetupBackendDynamicForm(FormMixinState, FormDynamicModelBackend):
    class Meta:
        fields = (
            'label', 'document_type', 'process_size', 'item_time_buffer',
            'state'
        )
        model = ImportSetup
