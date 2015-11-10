import os

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.wallpaper.helpers.file import file_hash


class Image(models.Model):
    uploaded_by = models.ForeignKey(User, blank=True, null=True)

    width = models.IntegerField(default=0, blank=True)
    height = models.IntegerField(default=0, blank=True)
    deleted = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)
    size = models.IntegerField(blank=True, default=0)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    hash = models.CharField(db_index=True, max_length=40)
    file = models.ImageField(upload_to='images/', null=False, blank=False)
    extension = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        index_together = [
            ['width', 'height'],
        ]

    def get_image_dimensions(self):
        return self.file.width, self.file.height

    def get_file_size(self):
        return self.file.size

    def get_file_hash(self):
        return file_hash(self.file)

    def save(self, **kwargs):
        # TODO hack. Issues with the file not being opened in some cases.
        if not self.hash:
            # Properties being extracted/generated for indexing purposes
            self.width, self.height = self.get_image_dimensions()
            self.size = self.get_file_size()
            self.hash = self.get_file_hash()
            self.extension = os.path.splitext(self.file.name)[1][1:]

        super(Image, self).save(**kwargs)


@receiver(pre_delete, sender=Image)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)
