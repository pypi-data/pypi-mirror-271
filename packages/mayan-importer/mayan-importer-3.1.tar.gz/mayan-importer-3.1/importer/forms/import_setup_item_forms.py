from django.utils.translation import ugettext_lazy as _

from mayan.apps.views import forms

from ..models import ImportSetupItem

from .form_mixins import FormMixinState


class ImportSetupItemForm(FormMixinState, forms.ModelForm):
    fieldsets = (
        (
            _('General'), {
                'fields': ('identifier', 'serialized_data')
            }
        ), (
            _(message='Processing'), {
                'fields': ('state',)
            }
        )
    )

    class Meta:
        fields = ('identifier', 'serialized_data', 'state')
        model = ImportSetupItem
