from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mayan.apps.documents.models.document_models import Document
from mayan.apps.events.decorators import method_event
from mayan.apps.events.event_managers import (
    EventManagerMethodAfter, EventManagerSave
)

from ..events import (
    event_import_setup_item_created, event_import_setup_item_deleted,
    event_import_setup_item_edited
)
from ..literals import (
    IMPORT_SETUP_ITEM_STATE_CHOICES, IMPORT_SETUP_ITEM_STATE_NONE
)

from .import_setup_item_model_mixins import ImportSetupItemBusinessLogicMixin
from .import_setup_models import ImportSetup
from .model_mixins import ModelMixinState, ModelMixinTaskMethod


class ImportSetupItem(
    ImportSetupItemBusinessLogicMixin, ModelMixinState, ModelMixinTaskMethod,
    models.Model
):
    import_setup = models.ForeignKey(
        on_delete=models.CASCADE, related_name='items',
        to=ImportSetup, verbose_name=_(message='Import setup')
    )
    identifier = models.CharField(
        db_index=True, help_text=_(
            message='Source data element that uniquely identifies a file to '
            'import.'
        ), max_length=64, verbose_name=_(message='Identifier')
    )
    serialized_data = models.TextField(
        blank=True, default='{}', help_text=_(
            message='Source data corresponding to a file to import.'
        ), verbose_name=_(message='Serialized data')
    )
    documents = models.ManyToManyField(
        blank=True, related_name='import_items', to=Document,
        verbose_name=_(message='Document')
    )

    class Meta:
        ordering = ('import_setup', 'identifier')
        state_choices = IMPORT_SETUP_ITEM_STATE_CHOICES
        state_default = IMPORT_SETUP_ITEM_STATE_NONE
        task_name_list = ('task_import_setup_item_process',)
        verbose_name = _(message='Import setup item')
        verbose_name_plural = _(message='Import setup items')

    def __str__(self):
        return self.identifier

    def get_absolute_url(self):
        return reverse(
            viewname='importer:import_setup_items_list', kwargs={
                'import_setup_id': self.import_setup.pk
            }
        )

    @method_event(
        event_manager_class=EventManagerMethodAfter,
        event=event_import_setup_item_deleted,
        action_object='self',
        target='import_setup'
    )
    def delete(self):
        return super().delete()

    @method_event(
        event_manager_class=EventManagerSave,
        created={
            'action_object': 'import_setup',
            'event': event_import_setup_item_created,
            'target': 'self'
        },
        edited={
            'action_object': 'import_setup',
            'event': event_import_setup_item_edited,
            'target': 'self'
        }
    )
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
