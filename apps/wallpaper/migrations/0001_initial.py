# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('width', models.IntegerField(default=0, blank=True)),
                ('height', models.IntegerField(default=0, blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('size', models.IntegerField(default=0, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hash', models.CharField(unique=True, max_length=40)),
                ('file', models.ImageField(upload_to=b'images/')),
                ('extension', models.CharField(max_length=5, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wallpaper.Image')),
            ],
            options={
            },
            bases=('wallpaper.image',),
        ),
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wallpaper.Image')),
                ('active', models.NullBooleanField(default=None)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('url', models.CharField(max_length=300, null=True, blank=True)),
            ],
            options={
            },
            bases=('wallpaper.image',),
        ),
        migrations.CreateModel(
            name='WallpaperFavorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='wallpaper_favorites', to=settings.AUTH_USER_MODEL)),
                ('wallpaper', models.ForeignKey(related_name='favorites', to='wallpaper.Wallpaper')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WallpaperRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(choices=[(1, b'Like'), (-1, b'Dislike')])),
                ('modified', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(related_name='wallpaper_ratings', to=settings.AUTH_USER_MODEL)),
                ('wallpaper', models.ForeignKey(related_name='ratings', to='wallpaper.Wallpaper')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='wallpaperrating',
            unique_together=set([('wallpaper', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='wallpaperfavorite',
            unique_together=set([('wallpaper', 'user')]),
        ),
        migrations.AddField(
            model_name='thumbnail',
            name='wallpaper',
            field=models.ForeignKey(related_name='thumbnails', to='wallpaper.Wallpaper'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='image',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
