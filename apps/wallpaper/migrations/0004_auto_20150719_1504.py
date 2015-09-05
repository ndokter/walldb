# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallpaper', '0003_auto_20150719_1500'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='image',
            index_together=set([('width', 'height')]),
        ),
    ]
