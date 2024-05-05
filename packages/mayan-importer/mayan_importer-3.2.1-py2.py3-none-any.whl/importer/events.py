from django.utils.translation import ugettext_lazy as _

from mayan.apps.events.classes import EventTypeNamespace

namespace = EventTypeNamespace(
    label=_(message='Importer'), name='importer'
)

# Import setup

event_import_setup_created = namespace.add_event_type(
    label=_(message='Import setup created'), name='import_setup_created'
)
event_import_setup_edited = namespace.add_event_type(
    label=_(message='Import setup edited'), name='import_setup_edited'
)
event_import_setup_populate_finished = namespace.add_event_type(
    label=_(message='Import setup populate ended'),
    name='import_setup_populate_finished'
)
event_import_setup_populate_started = namespace.add_event_type(
    label=_(message='Import setup populate started'),
    name='import_setup_populate_started'
)
event_import_setup_process_finished = namespace.add_event_type(
    label=_(message='Import setup process ended'),
    name='import_setup_process_finished'
)
event_import_setup_process_started = namespace.add_event_type(
    label=_(message='Import setup process started'),
    name='import_setup_process_started'
)

# Import setup item

event_import_setup_item_created = namespace.add_event_type(
    label=_(message='Import setup item created'),
    name='import_setup_item_created'
)
event_import_setup_item_deleted = namespace.add_event_type(
    label=_(message='Import setup item deleted'),
    name='import_setup_item_deleted'
)
event_import_setup_item_edited = namespace.add_event_type(
    label=_(message='Import setup item edited'),
    name='import_setup_item_edited'
)
event_import_setup_item_finished = namespace.add_event_type(
    label=_(message='Import setup item completed'),
    name='import_setup_item_finished'
)
