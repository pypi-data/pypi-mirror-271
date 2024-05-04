from django import forms as django_forms
from django.utils.translation import ugettext_lazy as _

from mayan.apps.views import forms


class ModelFilerUpload(forms.Form):
    uploaded_file = django_forms.FileField(
        help_text=_(message='CSV file that contain rows of model data.'),
        label=_(message='File')
    )
