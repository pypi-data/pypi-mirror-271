from django.db import migrations

IMPORT_SETUP_ITEM_STATE_COMPLETED = 5
IMPORT_SETUP_ITEM_STATE_PROCESSING = 6
IMPORT_SETUP_ITEM_STATE_PROCESSED = 7

IMPORT_SETUP_STATE_EXECUTING = 4
IMPORT_SETUP_STATE_COMPLETE = 5
IMPORT_SETUP_STATE_PROCESSING = 7
IMPORT_SETUP_STATE_PROCESSED = 8

IMPORT_SETUP_ITEM_STATE_MAP = {
    IMPORT_SETUP_ITEM_STATE_COMPLETED: IMPORT_SETUP_ITEM_STATE_PROCESSED,
    IMPORT_SETUP_STATE_EXECUTING: IMPORT_SETUP_STATE_PROCESSING
}

IMPORT_SETUP_STATE_MAP = {
    IMPORT_SETUP_STATE_COMPLETE: IMPORT_SETUP_STATE_PROCESSED,
    IMPORT_SETUP_STATE_EXECUTING: IMPORT_SETUP_STATE_PROCESSING
}


def code_import_setup_item_state_update(apps, schema_editor):
    ImportSetupItem = apps.get_model(
        app_label='importer', model_name='ImportSetupItem'
    )

    for key, value in IMPORT_SETUP_ITEM_STATE_MAP.items():
        queryset = ImportSetupItem.objects.filter(state=key)
        queryset.update(state=value)


def code_import_setup_item_state_update_reverse(apps, schema_editor):
    ImportSetupItem = apps.get_model(
        app_label='importer', model_name='ImportSetupItem'
    )

    for key, value in IMPORT_SETUP_ITEM_STATE_MAP.items():
        queryset = ImportSetupItem.objects.filter(state=value)
        queryset.update(state=key)


def code_import_setup_state_update(apps, schema_editor):
    ImportSetup = apps.get_model(
        app_label='importer', model_name='ImportSetup'
    )

    for key, value in IMPORT_SETUP_STATE_MAP.items():
        queryset = ImportSetup.objects.filter(state=key)
        queryset.update(state=value)


def code_import_setup_state_update_reverse(apps, schema_editor):
    ImportSetup = apps.get_model(
        app_label='importer', model_name='ImportSetup'
    )

    for key, value in IMPORT_SETUP_STATE_MAP.items():
        queryset = ImportSetup.objects.filter(state=value)
        queryset.update(state=key)


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0020_auto_20240502_1907')
    ]

    operations = [
        migrations.RunPython(
            code=code_import_setup_item_state_update,
            reverse_code=code_import_setup_item_state_update_reverse
        ),
        migrations.RunPython(
            code=code_import_setup_state_update,
            reverse_code=code_import_setup_state_update_reverse
        )
    ]

