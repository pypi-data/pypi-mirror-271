from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse, reverse_lazy
from django.utils.translation import ungettext, ugettext_lazy as _

from mayan.apps.backends.views import (
    ViewSingleObjectDynamicFormModelBackendCreate,
    ViewSingleObjectDynamicFormModelBackendEdit
)
from mayan.apps.views.generics import (
    FormView, MultipleObjectConfirmActionView, SingleObjectDeleteView,
    SingleObjectListView
)

from ..classes import ImportSetupBackend
from ..forms.import_setup_forms import (
    ImportSetupBackendSelectionForm, ImportSetupBackendDynamicForm
)
from ..icons.import_setup_icons import (
    icon_import_setup_backend_selection, icon_import_setup_clear,
    icon_import_setup_delete, icon_import_setup_edit, icon_import_setup_list,
    icon_import_setup_process_single, icon_import_setup_populate_single
)
from ..links.import_setup_links import link_import_setup_backend_selection
from ..models import ImportSetup
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view
)
from ..tasks import task_import_setup_populate, task_import_setup_process


class ImportSetupBackendSelectionView(FormView):
    extra_context = {
        'title': _(message='New import backend selection')
    }
    form_class = ImportSetupBackendSelectionForm
    view_icon = icon_import_setup_backend_selection
    view_permission = permission_import_setup_create

    def form_valid(self, form):
        backend = form.cleaned_data['backend']
        return HttpResponseRedirect(
            redirect_to=reverse(
                kwargs={'backend_path': backend},
                viewname='importer:import_setup_create'
            )
        )


class ImportSetupClearView(MultipleObjectConfirmActionView):
    model = ImportSetup
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_id'
    success_message = _(message='%(count)d import setup cleared.')
    success_message_plural = _(message='%(count)d import setups cleared.')
    view_icon = icon_import_setup_clear

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Clear the selected import setup?',
                plural='Clear the selected import setups?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        message='Clear import setup: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def object_action(self, instance, form=None):
        instance.do_clear()


class ImportSetupCreateView(ViewSingleObjectDynamicFormModelBackendCreate):
    backend_class = ImportSetupBackend
    form_class = ImportSetupBackendDynamicForm
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')
    view_icon = icon_import_setup_backend_selection
    view_permission = permission_import_setup_create

    def get_extra_context(self):
        backend_class = self.get_backend_class()
        return {
            'title': _(
                message='Create a "%s" import setup'
            ) % backend_class.label
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
            'backend_path': self.kwargs['backend_path']
        }


class ImportSetupDeleteView(SingleObjectDeleteView):
    model = ImportSetup
    object_permission = permission_import_setup_delete
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(viewname='importer:import_setup_list')
    view_icon = icon_import_setup_delete

    def get_extra_context(self):
        return {
            'import_setup': None,
            'object': self.object,
            'title': _(message='Delete the import setup: %s?') % self.object
        }


class ImportSetupEditView(ViewSingleObjectDynamicFormModelBackendEdit):
    form_class = ImportSetupBackendDynamicForm
    model = ImportSetup
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_id'
    view_icon = icon_import_setup_edit

    def get_extra_context(self):
        return {
            'object': self.object,
            'title': _(message='Edit import setup: %s') % self.object
        }

    def get_form_extra_kwargs(self):
        return {'user': self.request.user}

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}


class ImportSetupListView(SingleObjectListView):
    model = ImportSetup
    object_permission = permission_import_setup_view
    view_icon = icon_import_setup_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_import_setup_list,
            'no_results_main_link': link_import_setup_backend_selection.resolve(
                context=RequestContext(request=self.request)
            ),
            'no_results_text': _(
                message='Import setups are configuration units that will '
                'retrieve files for external locations and create documents '
                'from them.'
            ),
            'no_results_title': _(message='No import setups available'),
            'title': _(message='Import setups')
        }


class ImportSetupPopulateView(MultipleObjectConfirmActionView):
    model = ImportSetup
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )
    success_message = _(
        message='%(count)d import setup item population queued.'
    )
    success_message_plural = _(
        message='%(count)d import setups item population queued.'
    )
    view_icon = icon_import_setup_populate_single

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'message': _(
                message='This process will populate the items to import by '
                'querying the source repository. The process will run in the '
                'background and once starter, cannot be stopped from the '
                'user interface. The time to completion will depend on the '
                'number of files that match the import setup criteria, the '
                'import backend, the size of the source repository, and '
                'the bandwidth between Mayan EDMS and the source '
                'repository. The completion may take between a few minutes '
                'to a few days to complete.'
            ),
            'title': ungettext(
                singular='Population the selected import setup?',
                plural='Population the selected import setups?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        message='Prepare import setup: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def object_action(self, instance, form=None):
        task_import_setup_populate.apply_async(
            kwargs={'import_setup_id': instance.pk}
        )


class ImportSetupProcessView(MultipleObjectConfirmActionView):
    model = ImportSetup
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_id'
    post_action_redirect = reverse_lazy(
        viewname='importer:import_setup_list'
    )
    success_message = _(message='%(count)d import setup processing queued.')
    success_message_plural = _(
        message='%(count)d import setups processing queued.'
    )
    view_icon = icon_import_setup_process_single

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'title': ungettext(
                singular='Process the selected import setup?',
                plural='Process the selected import setups?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        message='Process import setup: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {'_event_actor': self.request.user}

    def object_action(self, instance, form=None):
        if instance.items.count() == 0:
            messages.warning(
                message=_(
                    message='Import setup "%s" does not have any item to '
                    'process. Use the prepare action first.'
                ) % instance, request=self.request
            )
        else:
            task_import_setup_process.apply_async(
                kwargs={'import_setup_id': instance.pk}
            )
