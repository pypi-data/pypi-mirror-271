from django.utils.translation import ugettext_lazy as _

from mayan.apps.navigation.classes import Link

from ..icons.import_setup_filer_icons import (
    icon_import_setup_filer_load, icon_import_setup_filer_save
)
from ..permissions import (
    permission_model_filer_load, permission_model_filer_save
)


def conditional_disable_import_has_items(context):
    return context['resolved_object'].items.count() == 0


def conditional_import_setup_item_process_allowed(context):
    return not context['resolved_object'].get_process_allowed()


link_model_filer_load = Link(
    args='resolved_object.pk', icon=icon_import_setup_filer_load,
    permissions=(permission_model_filer_load,),
    text=_(message='Load items'), view='importer:import_setup_load'
)
link_model_filer_save = Link(
    args='resolved_object.pk', icon=icon_import_setup_filer_save,
    permissions=(permission_model_filer_save,),
    text=_(message='Save items'), view='importer:import_setup_save'
)
