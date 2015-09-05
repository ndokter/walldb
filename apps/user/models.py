import os
import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)

    return os.path.join('avatars/', filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='walldb_profile')

    is_public = models.BooleanField(
        default=True,
        verbose_name=_('Allow other users to view my profile')
    )
    avatar = models.ImageField(upload_to=get_file_path, blank=True, null=True)
