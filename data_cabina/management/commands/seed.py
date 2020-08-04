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
        print('Seeding cabins')
        self.seed_cabins()
        #
        print('Seeding captures')
        self.seed_captures()
        #
        print('Done.')

    def seed_company(self):
        print('Seeding companies')
        n = random.randint(0, 100)
        self.company = Company(name='Company ' + str(n),
                               description='Description ' + str(n))
        self.company.save()

    def seed_user(self):
        try:
            user = User.objects.get(username='test1')
        except:
            self.seed_company()
            self.user = User(username='test1')
            self.user.set_password("test_password")
            self.user.save()
            client = Client.objects.create(user=self.user,company=self.company)
        else:
            self.user = user
            self.company = self.user.client.company

    def seed_cabins(self):
        num_cabins = 5
        self.cabins = []
        for i in range(num_cabins):
            n = random.randint(0, 10000)
            token = CabinToken.objects.create(is_used = True)
            cabin = Cabin(company=self.company, token = token)
            cabin.save()
            self.cabins.append(cabin)

    def seed_captures(self):
        num_captures = 5
        for cabin in self.cabins:
            for i in range(num_captures):
                temp = random.uniform(36, 43)
                is_wearing_mask = random.uniform(0, 1) > 0.5
                is_image_saved = True
                image_base64 = self.create_image()

                capture = Capture(cabin=cabin,
                                  temp=temp,
                                  is_wearing_mask=is_wearing_mask,
                                  is_image_saved=is_image_saved)
                capture.save()
                capture.image.save(str(capture.id) + '.txt', image_base64)

    def create_image(self, width=512, height=256):
        rgb_array = numpy.random.rand(int(height), int(width), 3) * 255
        image = Image.fromarray(rgb_array.astype('uint8')).convert('RGB')
        image_bytes = io.BytesIO()
        image.save(image_bytes, "JPEG")
        img_str = base64.b64encode(image_bytes.getvalue())
        image_bytes = io.BytesIO()
        image_bytes.write(img_str)
        return image_bytes
