from django.utils.translation import ugettext_lazy as _

from mayan.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(
    label=_(message='Importer'), name='importer'
)

# Documents

permission_import_setup_metadata_view = namespace.add_permission(
    label=_('View document import setup metadata'),
    name='import_setup_metadata_view'
)

# Import setup

permission_import_setup_create = namespace.add_permission(
    label=_(message='Create import setups'), name='import_setup_create'
)
permission_import_setup_delete = namespace.add_permission(
    label=_(message='Delete import setups'), name='import_setup_delete'
)
permission_import_setup_edit = namespace.add_permission(
    label=_(message='Edit import setups'), name='import_setup_edit'
)
permission_import_setup_process = namespace.add_permission(
    label=_(message='Process import setups'), name='import_setup_process'
)
permission_import_setup_view = namespace.add_permission(
    label=_(message='View import setups'), name='import_setup_view'
)

namespace = PermissionNamespace(
    label=_(message='Model filer'), name='model_filer'
)

permission_model_filer_load = namespace.add_permission(
    label=_(message='Save models to load'), name='model_filer_load'
)
permission_model_filer_save = namespace.add_permission(
    label=_(message='Save models to file'), name='model_filer_save'
)
