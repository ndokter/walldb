# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0005_auto_20150719_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='hash',
            field=models.CharField(max_length=40, db_index=True),
        ),
    ]
