from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons.import_setup_item_icons import (
    icon_import_setup_item_delete_multiple,
    icon_import_setup_item_delete_single,
    icon_import_setup_item_document_list,
    icon_import_setup_item_edit, icon_import_setup_item_process_multiple,
    icon_import_setup_item_process_single, icon_import_setup_items_list
)
from ..permissions import (
    permission_import_setup_edit, permission_import_setup_process,
    permission_import_setup_view
)


def conditional_disable_import_has_items(context):
    return context['resolved_object'].items.count() == 0


def conditional_import_setup_item_process_allowed(context):
    return not context['resolved_object'].get_process_allowed()


link_import_setup_item_delete_single = Link(
    args='resolved_object.pk', icon=icon_import_setup_item_delete_single,
    permissions=(permission_import_setup_edit,),
    tags='dangerous', text=_(message='Delete'),
    view='importer:import_setup_item_delete_single'
)
link_import_setup_item_delete_multiple = Link(
    icon=icon_import_setup_item_delete_multiple,
    permissions=(permission_import_setup_edit,),
    tags='dangerous', text=_(message='Delete'),
    view='importer:import_setup_item_delete_multiple'
)
link_import_setup_item_document_list = Link(
    args='resolved_object.pk',
    icon=icon_import_setup_item_document_list,
    permissions=(permission_import_setup_view,), text=_(message='Documents'),
    view='importer:import_setup_item_document_list'
)
link_import_setup_item_edit = Link(
    args='resolved_object.pk', icon=icon_import_setup_item_edit,
    permissions=(permission_import_setup_edit,), text=_(message='Edit'),
    view='importer:import_setup_item_edit'
)
link_import_setup_item_list = Link(
    args='resolved_object.pk',
    icon=icon_import_setup_items_list,
    permissions=(permission_import_setup_view,), text=_(message='Items'),
    view='importer:import_setup_items_list'
)
link_import_setup_item_process_multiple = Link(
    icon=icon_import_setup_item_process_multiple,
    text=_(message='Process'),
    view='importer:import_setup_item_process_multiple'
)
link_import_setup_item_process_single = Link(
    args='resolved_object.pk',
    conditional_disable=conditional_import_setup_item_process_allowed,
    icon=icon_import_setup_item_process_single,
    permissions=(permission_import_setup_process,),
    text=_(message='Process'),
    view='importer:import_setup_item_process_single'
)
