from django.template import RequestContext
from django.urls import reverse
from django.utils.translation import ungettext, ugettext_lazy as _

from mayan.apps.documents.views.document_views import DocumentListView
from mayan.apps.views.generics import (
    MultipleObjectConfirmActionView, SingleObjectEditView,
    SingleObjectListView
)
from mayan.apps.views.view_mixins import ExternalObjectViewMixin

from ..forms.import_setup_item_forms import ImportSetupItemForm
from ..icons.import_setup_item_icons import (
    icon_import_setup_item_delete_single,
    icon_import_setup_item_document_list, icon_import_setup_item_edit,
    icon_import_setup_items_list, icon_import_setup_item_process_single
)
from ..links.import_setup_filer_links import link_model_filer_load
from ..links.import_setup_links import link_import_setup_populate_single
from ..models import ImportSetup, ImportSetupItem
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view
)


class ImportSetupItemDeleteView(MultipleObjectConfirmActionView):
    model = ImportSetupItem
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_item_id'
    success_message = _(message='%(count)d import setup item deleted.')
    success_message_plural = _(
        message='%(count)d import setup items deleted.'
    )
    view_icon = icon_import_setup_item_delete_single

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'delete_view': True,
            'import_setup': self.object_list.first().import_setup,
            'message': _(
                message='You can add this item again by executing the '
                'prepare action.'
            ),
            'navigation_object_list': ('import_setup', 'object'),
            'title': ungettext(
                singular='Delete the selected import setup item?',
                plural='Delete the selected import setup items?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        message='Delete import setup item: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        # Use [0] instead of first(). First returns None and it is not usable.
        return reverse(
            viewname='importer:import_setup_items_list', kwargs={
                'import_setup_id': self.object_list[0].import_setup.pk
            }
        )

    def object_action(self, instance, form=None):
        instance.delete()


class ImportSetupItemEditView(SingleObjectEditView):
    form_class = ImportSetupItemForm
    model = ImportSetupItem
    object_permission = permission_import_setup_edit
    pk_url_kwarg = 'import_setup_item_id'
    view_icon = icon_import_setup_item_edit

    def get_extra_context(self):
        return {
            'import_setup': self.object.import_setup,
            'navigation_object_list': ('import_setup', 'object'),
            'title': _(message='Edit import setup item: %s') % self.object
        }

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user
        }


class ImportSetupItemDocumentListView(
    ExternalObjectViewMixin, DocumentListView
):
    external_object_class = ImportSetupItem
    external_object_permission = permission_import_setup_view
    external_object_pk_url_kwarg = 'import_setup_item_id'
    view_icon = icon_import_setup_item_document_list

    def get_document_queryset(self):
        return self.external_object.documents.all()

    def get_extra_context(self):
        context = super().get_extra_context()
        context.update(
            {
                'import_setup': self.external_object.import_setup,
                'import_setup_item': self.external_object,
                'navigation_object_list': (
                    'import_setup', 'import_setup_item'
                ),
                'no_results_text': _(
                    message='This view will list the documents that were '
                    'created by an import setup item.'
                ),
                'no_results_title': _(
                    message='There are no documents for this import setup '
                    'item.'
                ),
                'title': _(
                    message='Document created from import setup item: %s'
                ) % self.external_object
            }
        )
        return context


class ImportSetupItemListView(ExternalObjectViewMixin, SingleObjectListView):
    external_object_class = ImportSetup
    external_object_permission = permission_import_setup_view
    external_object_pk_url_kwarg = 'import_setup_id'
    view_icon = icon_import_setup_items_list

    def get_extra_context(self):
        return {
            'hide_link': True,
            'hide_object': True,
            'no_results_icon': icon_import_setup_items_list,
            'no_results_secondary_links': (
                link_import_setup_populate_single.resolve(
                    context=RequestContext(
                        dict_={'object': self.external_object},
                        request=self.request
                    )
                ),
                link_model_filer_load.resolve(
                    context=RequestContext(
                        dict_={'object': self.external_object},
                        request=self.request
                    )
                ),
            ),
            'no_results_text': _(
                message='Import setups items are the entries for the actual '
                'files that will be imported and converted into documents.'
            ),
            'no_results_title': _(message='No import setups items available'),
            'object': self.external_object,
            'title': _(
                message='Items of import setup: %s'
            ) % self.external_object
        }

    def get_source_queryset(self):
        return self.external_object.items.all()


class ImportSetupItemProcessView(MultipleObjectConfirmActionView):
    model = ImportSetupItem
    object_permission = permission_import_setup_process
    pk_url_kwarg = 'import_setup_item_id'
    success_message = _(message='%(count)d import setup item processed.')
    success_message_plural = _(
        message='%(count)d import setup items processed.'
    )
    view_icon = icon_import_setup_item_process_single

    def get_extra_context(self):
        queryset = self.object_list

        result = {
            'import_setup': self.object_list.first().import_setup,
            'navigation_object_list': ('import_setup', 'object'),
            'title': ungettext(
                singular='Process the selected import setup item?',
                plural='Process the selected import setup items?',
                number=queryset.count()
            )
        }

        if queryset.count() == 1:
            result.update(
                {
                    'object': queryset.first(),
                    'title': _(
                        message='Process import setup item: %s'
                    ) % queryset.first()
                }
            )

        return result

    def get_instance_extra_data(self):
        return {
            '_event_actor': self.request.user,
        }

    def get_post_action_redirect(self):
        # Use [0] instead of first(). First returns None and it is not usable.
        return reverse(
            viewname='importer:import_setup_items_list', kwargs={
                'import_setup_id': self.object_list[0].import_setup.pk
            }
        )

    def object_action(self, instance, form=None):
        instance.queue_task_import_setup_item_process(
            kwargs={'import_setup_item_id': instance.pk}
        )
