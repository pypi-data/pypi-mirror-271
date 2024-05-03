from django.db import migrations

IMPORT_SETUP_ITEM_STATE_COMPLETED = 5
IMPORT_SETUP_ITEM_STATE_PROCESSING = 6
IMPORT_SETUP_ITEM_STATE_PROCESSED = 7

IMPORT_SETUP_STATE_EXECUTING = 4
IMPORT_SETUP_STATE_COMPLETE = 5
IMPORT_SETUP_STATE_PROCESSING = 7
IMPORT_SETUP_STATE_PROCESSED = 8


def code_import_setup_item_state_update(apps, schema_editor):
    ImportSetupItem = apps.get_model(
        app_label='importer', model_name='ImportSetupItem'
    )

    import_setup_item_state_map = {
        IMPORT_SETUP_ITEM_STATE_COMPLETED: IMPORT_SETUP_ITEM_STATE_PROCESSED,
        IMPORT_SETUP_STATE_EXECUTING: IMPORT_SETUP_STATE_PROCESSING
    }

    for key, value in import_setup_item_state_map.items():
        queryset = ImportSetupItem.objects.filter(state=key)
        queryset.update(state=value)


def code_import_setup_state_update(apps, schema_editor):
    ImportSetup = apps.get_model(
        app_label='importer', model_name='ImportSetup'
    )

    import_setup_state_map = {
        IMPORT_SETUP_STATE_COMPLETE: IMPORT_SETUP_STATE_PROCESSED,
        IMPORT_SETUP_STATE_EXECUTING: IMPORT_SETUP_STATE_PROCESSING
    }

    for key, value in import_setup_state_map.items():
        queryset = ImportSetup.objects.filter(state=key)
        queryset.update(state=value)


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0020_auto_20240502_1907')
    ]

    operations = [
        migrations.RunPython(
            code=code_import_setup_item_state_update
        ),
        migrations.RunPython(
            code=code_import_setup_state_update
        )
    ]
