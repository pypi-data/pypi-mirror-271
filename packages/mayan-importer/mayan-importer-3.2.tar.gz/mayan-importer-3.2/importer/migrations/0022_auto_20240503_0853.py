from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0021_migrate_state_codes')
    ]

    operations = [
        migrations.AlterField(
            model_name='importsetup', name='state',
            field=models.PositiveIntegerField(
                blank=True, help_text="The current condition or "
                "configuration of the object. This is managed automatically "
                "by the system. Only change the state if the object's task "
                "is stale or orphaned.", verbose_name='State'
            )
        ),
        migrations.AlterField(
            model_name='importsetupitem', name='state',
            field=models.PositiveIntegerField(
                blank=True, help_text="The current condition or "
                "configuration of the object. This is managed automatically "
                "by the system. Only change the state if the object's task "
                "is stale or orphaned.", verbose_name='State'
            )
        )
    ]
