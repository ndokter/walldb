from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from apps.user.models import UserProfile


class Command(BaseCommand):
    help = 'Create profiles for users that dont have one yet.'

    def handle(self, *args, **options):
        for user in User.objects.filter(walldb_profile=None):
            UserProfile(user=user).save()
