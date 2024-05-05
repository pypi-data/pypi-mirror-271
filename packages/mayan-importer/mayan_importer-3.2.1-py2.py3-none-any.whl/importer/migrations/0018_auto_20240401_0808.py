from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0017_delete_importsetuplog')
    ]

    operations = [
        migrations.RemoveField(
            model_name='importsetup', name='credential',
        ),
        migrations.RemoveField(
            model_name='importsetupitem', name='state_data',
        ),
        migrations.AlterField(
            field=models.PositiveIntegerField(
                choices=[(1, 'Idle'), (2, 'Error'), (3, 'Populating'), (4, 'Executing')], default=1, help_text='The last recorded state of the import setup.', verbose_name='State'
            ), model_name='importsetup', name='state',
        ),
        migrations.AlterField(
            field=models.IntegerField(choices=[(1, 'Idle'), (2, 'Error'), (3, 'Queued'), (4, 'Downloaded'), (5, 'Complete'), (6, 'Processing')], db_index=True, default=1, verbose_name='State'),
            model_name='importsetupitem', name='state',
        ),
        migrations.DeleteModel(name='ImportSetupAction'),
    ]
