import random, time, io, base64
import numpy
from PIL import Image
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from data_cabina.models import *
from auth_cabina.models import *


class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        print('Starting seeding...')
        #
        print('Seeding user')
        self.seed_user()
        #
        print('Done.')

    def seed_user(self):
        try:
            user = User.objects.get(username='admin')
        except:
            User.objects.create_superuser('admin', 'admin@example.com', 'azteca2020')
