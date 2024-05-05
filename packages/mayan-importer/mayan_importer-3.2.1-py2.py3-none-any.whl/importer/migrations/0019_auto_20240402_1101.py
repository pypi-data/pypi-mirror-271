from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0018_auto_20240401_0808')
    ]

    operations = [
        migrations.AlterField(
            model_name='importsetup', name='state',
            field=models.PositiveIntegerField(
                choices=[(1, 'None'), (2, 'Error'), (3, 'Populating'), (4, 'Executing')], default=1, help_text='The last recorded state of the import setup.', verbose_name='State'
            ),
        ),
        migrations.AlterField(
            model_name='importsetupitem', name='identifier',
            field=models.CharField(db_index=True, help_text='Source data element that uniquely identifies a file to import.', max_length=64, verbose_name='Identifier'),
        ),
        migrations.AlterField(
            model_name='importsetupitem', name='serialized_data',
            field=models.TextField(blank=True, default='{}', help_text='Source data corresponding to a file to import.', verbose_name='Serialized data'),
        ),
        migrations.AlterField(
            model_name='importsetupitem', name='state',
            field=models.IntegerField(choices=[(1, 'None'), (2, 'Error'), (3, 'Queued'), (5, 'Complete'), (6, 'Processing')], db_index=True, default=1, verbose_name='State'),
        ),
    ]
