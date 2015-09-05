# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0006_auto_20150719_1519'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='wallpaperrating',
            name='score',
            field=models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')]),
        ),
    ]
