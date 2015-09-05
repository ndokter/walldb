# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0004_auto_20150719_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallpaper',
            name='active',
            field=models.NullBooleanField(default=None, db_index=True),
        ),
    ]
