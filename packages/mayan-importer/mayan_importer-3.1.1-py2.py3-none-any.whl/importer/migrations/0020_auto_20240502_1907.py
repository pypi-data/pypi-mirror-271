from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0019_auto_20240402_1101')
    ]

    operations = [
        migrations.AlterField(
            model_name='importsetup', name='state',
            field=models.PositiveIntegerField(
                choices=[
                    (5, 'Complete'), (2, 'Error'), (4, 'Executing'),
                    (1, 'None'), (6, 'Populated'), (3, 'Populating'),
                    (8, 'Processed'), (7, 'Processing')
                ], default=1, help_text='The current condition or '
                'configuration of the import setup. This is managed '
                'automatically by the system. Only change the state if the '
                'import setup is stale or orphaned.', verbose_name='State'
            )
        ),
        migrations.AlterField(
            model_name='importsetupitem', name='state',
            field=models.IntegerField(
                choices=[
                    (5, 'Complete'), (2, 'Error'), (1, 'None'),
                    (7, 'Processed'), (6, 'Processing'), (3, 'Queued')
                ], db_index=True, default=1, help_text='The current '
                'condition or configuration of the item. This is managed '
                'automatically by the system. Only change the state if the '
                'item is stale or orphaned.', verbose_name='State'
            )
        )
    ]
