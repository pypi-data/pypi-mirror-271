import logging

from django.utils.translation import ugettext_lazy as _

from mayan.apps.acls.classes import ModelPermission
from mayan.apps.common.apps import MayanAppConfig
from mayan.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_related, menu_return,
    menu_secondary, menu_setup
)
from mayan.apps.credentials.links import link_credential_list
from mayan.apps.events.classes import EventModelRegistry, ModelEventType
from mayan.apps.logging.classes import ErrorLog
from mayan.apps.navigation.classes import SourceColumn
from mayan.apps.views.column_widgets import TwoStateWidget

from .classes import ImportSetupBackend, ModelFiler
from .events import (
    event_import_setup_edited, event_import_setup_item_finished,
    event_import_setup_item_deleted, event_import_setup_item_edited,
    event_import_setup_process_finished, event_import_setup_process_started,
    event_import_setup_populate_finished, event_import_setup_populate_started
)
from .links.import_setup_filer_links import (
    link_model_filer_load, link_model_filer_save
)
from .links.import_setup_item_links import (
    link_import_setup_item_delete_multiple,
    link_import_setup_item_delete_single,
    link_import_setup_item_document_list, link_import_setup_item_edit,
    link_import_setup_item_list, link_import_setup_item_process_multiple,
    link_import_setup_item_process_single
)
from .links.import_setup_links import (
    link_import_setup_backend_selection, link_import_setup_clear_multiple,
    link_import_setup_clear_single, link_import_setup_delete,
    link_import_setup_edit, link_import_setup_list,
    link_import_setup_populate_multiple, link_import_setup_populate_single,
    link_import_setup_process_multiple, link_import_setup_process_single,
    link_import_setups
)
from .permissions import (
    permission_import_setup_delete, permission_import_setup_edit,
    permission_import_setup_process, permission_import_setup_view,
    permission_model_filer_load, permission_model_filer_save
)

logger = logging.getLogger(name=__name__)


class ImporterApp(MayanAppConfig):
    app_namespace = 'importer'
    app_url = 'importer'
    has_rest_api = True
    has_tests = True
    name = 'importer'
    verbose_name = _(message='Importer')

    def ready(self):
        super().ready()

        ImportSetupBackend.load_modules()

        ImportSetup = self.get_model(model_name='ImportSetup')
        ImportSetupItem = self.get_model(model_name='ImportSetupItem')

        error_log = ErrorLog(app_config=self)
        error_log.register_model(model=ImportSetup, register_permission=True)
        error_log.register_model(model=ImportSetupItem)

        EventModelRegistry.register(model=ImportSetup)
        EventModelRegistry.register(model=ImportSetupItem)

        ModelEventType.register(
            model=ImportSetup, event_types=(
                event_import_setup_edited, event_import_setup_item_deleted,
                event_import_setup_populate_finished,
                event_import_setup_populate_started,
                event_import_setup_process_finished,
                event_import_setup_process_started
            )
        )
        ModelEventType.register(
            model=ImportSetupItem, event_types=(
                event_import_setup_item_finished,
                event_import_setup_item_edited
            )
        )

        ModelFiler(model=ImportSetupItem)

        ModelPermission.register(
            model=ImportSetup, permissions=(
                permission_import_setup_delete, permission_import_setup_edit,
                permission_import_setup_process, permission_import_setup_view,
                permission_model_filer_load, permission_model_filer_save
            )
        )

        ModelPermission.register_inheritance(
            model=ImportSetupItem, related='import_setup',
        )

        # Import setup

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=ImportSetup
        )
        SourceColumn(
            attribute='get_backend_class_label', include_label=True,
            source=ImportSetup
        )
        SourceColumn(
            attribute='get_item_processed_percent', empty_value=_(message='0%'),
            include_label=True, source=ImportSetup
        )
        SourceColumn(
            attribute='get_state_label', include_label=True,
            is_sortable=True, sort_field='state', source=ImportSetup
        )
        SourceColumn(
            attribute='get_process_allowed', include_label=True,
            source=ImportSetup, widget=TwoStateWidget
        )

        # Import setup item

        SourceColumn(
            attribute='identifier', is_identifier=True, is_sortable=True,
            source=ImportSetupItem
        )
        SourceColumn(
            attribute='serialized_data', include_label=True,
            source=ImportSetupItem
        )
        SourceColumn(
            attribute='get_state_label', include_label=True, is_sortable=True,
            sort_field='state', source=ImportSetupItem
        )

        # Import setup

        menu_list_facet.bind_links(
            links=(link_import_setup_item_list,), sources=(ImportSetup,)
        )

        menu_multi_item.bind_links(
            links=(
                link_import_setup_clear_multiple,
                link_import_setup_populate_multiple,
                link_import_setup_process_multiple
            ), sources=(ImportSetup,)
        )

        menu_object.bind_links(
            links=(
                link_import_setup_delete, link_import_setup_edit,
                link_import_setup_process_single
            ), sources=(ImportSetup,)
        )

        menu_related.bind_links(
            links=(link_credential_list,),
            sources=(
                ImportSetup, ImportSetupItem,
                'importer:import_setup_backend_selection',
                'importer:import_setup_create', 'importer:import_setup_list'
            )
        )

        menu_return.bind_links(
            links=(link_import_setup_list,), sources=(
                ImportSetup, ImportSetupItem,
                'importer:import_setup_backend_selection',
                'importer:import_setup_create', 'importer:import_setup_list'
            )
        )

        menu_secondary.bind_links(
            links=(link_import_setup_backend_selection,),
            sources=(
                ImportSetup, 'importer:import_setup_items_list',
                'importer:import_setup_create', 'importer:import_setup_list'
            )
        )

        menu_secondary.bind_links(
            links=(
                link_import_setup_clear_single,
                link_import_setup_populate_single, link_model_filer_load,
                link_model_filer_save
            ),
            sources=(
                'importer:import_setup_load',
                'importer:import_setup_items_list',
                'importer:import_setup_populate', 'importer:import_setup_save'
            )
        )

        menu_setup.bind_links(
            links=(link_import_setups,)
        )

        # Import setup item

        menu_list_facet.bind_links(
            links=(
                link_import_setup_item_document_list,
            ), sources=(ImportSetupItem,)
        )
        menu_multi_item.bind_links(
            links=(
                link_import_setup_item_delete_multiple,
                link_import_setup_item_process_multiple
            ), sources=(ImportSetupItem,)
        )
        menu_object.bind_links(
            links=(
                link_import_setup_item_delete_single,
                link_import_setup_item_edit,
                link_import_setup_item_process_single
            ), sources=(ImportSetupItem,)
        )
