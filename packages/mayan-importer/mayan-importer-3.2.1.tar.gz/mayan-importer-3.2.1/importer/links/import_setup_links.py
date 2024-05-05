from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link
from mayan.apps.navigation.utils import factory_condition_queryset_access

from ..icons.import_setup_icons import (
    icon_import_setup_backend_selection, icon_import_setup_clear,
    icon_import_setup_delete, icon_import_setup_edit,
    icon_import_setup_process_multiple, icon_import_setup_process_single,
    icon_import_setup_list, icon_import_setup_populate_multiple,
    icon_import_setup_populate_single
)
from ..permissions import (
    permission_import_setup_create, permission_import_setup_delete,
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view
)


def conditional_disable_process(context):
    return not context['resolved_object'].get_process_allowed()


def conditional_disable_clear_single(context):
    return context['resolved_object'].items.count() == 0


link_import_setup_backend_selection = Link(
    icon=icon_import_setup_backend_selection,
    permissions=(permission_import_setup_create,),
    text=_(message='Create import setup'),
    view='importer:import_setup_backend_selection',
)
link_import_setup_clear_multiple = Link(
    icon=icon_import_setup_clear, text=_(message='Clear items'),
    view='importer:import_setup_multiple_clear'
)
link_import_setup_clear_single = Link(
    args='resolved_object.pk',
    conditional_disable=conditional_disable_clear_single,
    icon=icon_import_setup_clear,
    permissions=(permission_import_setup_process,),
    text=_(message='Clear items'), view='importer:import_setup_clear'
)
link_import_setup_delete = Link(
    args='resolved_object.pk',
    icon=icon_import_setup_delete,
    permissions=(permission_import_setup_delete,),
    tags='dangerous', text=_(message='Delete'),
    view='importer:import_setup_delete'
)
link_import_setup_edit = Link(
    args='resolved_object.pk',
    icon=icon_import_setup_edit,
    permissions=(permission_import_setup_edit,), text=_(message='Edit'),
    view='importer:import_setup_edit'
)
link_import_setup_list = Link(
    icon=icon_import_setup_list,
    text=_(message='Import setup list'),
    view='importer:import_setup_list'
)
link_import_setup_populate_multiple = Link(
    icon=icon_import_setup_populate_multiple,
    text=_(message='Populate items'),
    view='importer:import_setup_populate_multiple'
)
link_import_setup_populate_single = Link(
    args='resolved_object.pk',
    icon=icon_import_setup_populate_single,
    permissions=(permission_import_setup_process,),
    text=_(message='Populate items'),
    view='importer:import_setup_populate_single'
)
link_import_setup_process_multiple = Link(
    icon=icon_import_setup_process_multiple, text=_(message='Process'),
    view='importer:import_setup_process_multiple'
)
link_import_setup_process_single = Link(
    args='resolved_object.pk',
    conditional_disable=conditional_disable_process,
    icon=icon_import_setup_process_single,
    permissions=(permission_import_setup_process,), text=_(message='Process'),
    view='importer:import_setup_process_single'
)
link_import_setups = Link(
    condition=factory_condition_queryset_access(
        app_label='importer', model_name='ImportSetup',
        object_permission=permission_import_setup_view,
        view_permission=permission_import_setup_create,
    ), icon=icon_import_setup_list,
    text=_(message='Importer'),
    view='importer:import_setup_list'
)
