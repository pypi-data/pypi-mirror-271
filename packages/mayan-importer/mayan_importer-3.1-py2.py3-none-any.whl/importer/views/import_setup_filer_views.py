from django.contrib import messages
from django.core.files import File
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.organizations.utils import get_organization_installation_url
from mayan.apps.storage.models import SharedUploadedFile
from mayan.apps.views.generics import ConfirmView, FormView
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from ..classes import ModelFiler
from ..forms.filer_forms import ModelFilerUpload
from ..icons.import_setup_filer_icons import (
    icon_import_setup_filer_load, icon_import_setup_filer_save
)
from ..models import ImportSetup
from ..permissions import (
    permission_model_filer_load, permission_model_filer_save
)
from ..tasks import task_model_filer_load, task_model_filer_save


class ImportSetupFilerLoadView(ExternalObjectViewMixin, FormView):
    external_object_class = ImportSetup
    external_object_object_permission = permission_model_filer_load
    external_object_pk_url_kwarg = 'import_setup_id'
    form_class = ModelFilerUpload
    view_icon = icon_import_setup_filer_load

    def form_valid(self, form):
        with self.request.FILES['uploaded_file'].open(mode='r') as file_object:
            shared_upload_file = SharedUploadedFile.objects.create(
                file=File(file_object),
            )

        full_model_name = ModelFiler.get_full_model_name(
            model=self.external_object.items.model
        )
        task_model_filer_load.apply_async(
            kwargs={
                'field_defaults': {'import_setup_id': self.external_object.pk},
                'full_model_name': full_model_name,
                'shared_upload_file_id': shared_upload_file.pk
            }
        )

        messages.success(
            message=_(
                message='File uploaded and queued for loading as models.'
            ), request=self.request
        )
        return HttpResponseRedirect(
            redirect_to=reverse(viewname='importer:import_setup_list')
        )

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                message='Load the items of import setup: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class ImportSetupFilerSaveConfirmView(ExternalObjectViewMixin, ConfirmView):
    external_object_class = ImportSetup
    external_object_object_permission = permission_model_filer_save
    external_object_pk_url_kwarg = 'import_setup_id'
    view_icon = icon_import_setup_filer_save

    def get_extra_context(self):
        return {
            'object': self.external_object,
            'title': _(
                message='Save the items of import setup: %s'
            ) % self.external_object
        }

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def view_action(self):
        full_model_name = ModelFiler.get_full_model_name(
            model=self.external_object.items.model
        )

        task_model_filer_save.apply_async(
            kwargs={
                'filter_kwargs': {'import_setup': self.external_object.pk},
                'full_model_name': full_model_name,
                'save_file_title': str(
                    _(message='Import setup "%s"') % self.external_object
                ),
                'organization_installation_url': get_organization_installation_url(
                    request=self.request
                ),
                'user_id': self.request.user.pk
            }
        )
