from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('importer', '0016_importsetup_item_time_buffer')
    ]

    operations = [
        migrations.DeleteModel(name='ImportSetupLog')
    ]
