# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='hash',
            field=models.CharField(max_length=40),
        ),
    ]
