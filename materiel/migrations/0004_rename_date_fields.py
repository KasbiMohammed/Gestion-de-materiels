# -*- coding: utf-8 -*-
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('materiel', '0003_add_vehicle_fields'),
    ]

    operations = [
        # Renommage des champs
        migrations.RenameField(
            model_name='materiel',
            old_name='date',
            new_name='date_entree',
        ),
        migrations.RenameField(
            model_name='materiel',
            old_name='date_reception',
            new_name='date_sortie',
        ),
    ]
