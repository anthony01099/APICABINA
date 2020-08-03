import random, time, io
import numpy
from PIL import Image
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from  django.core.files.images import ImageFile
from data_cabina.models import *

class Command(BaseCommand):
    help = 'Seeds the database.'

    def handle(self, *args, **options):
        print('Starting seeding...')
        #
        print('Seeding user')
        self.seed_user()
        #
        print('Seeding companies')
        self.seed_company()
        #
        print('Seeding cabins')
        self.seed_cabins()
        #
        print('Seeding captures')
        self.seed_captures()
        #
        print('Done.')

    def seed_user(self):
        try:
            user = User.objects.get(username = 'test')
        except:
            self.user = User(username = 'test', password = 'test_password')
            self.user.save()
        else:
            self.user = user

    def seed_company(self):
        n = random.randint(0,100)
        self.company = Company(name = 'Company ' + str(n),
                          description = 'Description ' + str(n))
        self.company.save()
        self.company.users.add(self.user)
        self.company.save()

    def seed_cabins(self):
        num_cabins = 5
        self.cabins = []
        for i in range(num_cabins):
            n = random.randint(0,10000)
            cabin = Cabin(company = self.company)
            cabin.save()
            self.cabins.append(cabin)

    def seed_captures(self):
        num_captures = 5
        for cabin in self.cabins:
            for i in range(num_captures):
                temp = random.uniform(36,43)
                is_wearing_mask = random.uniform(0,1) > 0.5
                is_image_saved = True
                image = self.create_image()
                capture = Capture(cabin = cabin,
                                  temp = temp,
                                  is_wearing_mask = is_wearing_mask,
                                  is_image_saved = is_image_saved)
                capture.save()
                capture.image.save(str(capture.id) + '.jpg', image)

    def create_image(self, width = 512, height = 256):
        rgb_array = numpy.random.rand(int(height) ,int(width),3) * 255
        image = Image.fromarray(rgb_array.astype('uint8')).convert('RGB')
        image = io.BytesIO(image.tobytes())
        file = ImageFile(image)
        return file
