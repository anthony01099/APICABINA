import json, random, numpy, base64
from PIL import Image
from django.test import TestCase, Client
from .models import *
from auth_cabina.models import Client as User_client
from .views import *


class DataCabinaTestCase(TestCase):
    """
        Test cabin registering in the system using a token.
    """
    def setUp(self):
        #Create a company
        self.company = Company.objects.create(name='Company ', description='Description')
        #Create a user
        self.user = User(username='test')
        self.user.set_password("test_password")
        self.user.save()
        client = User_client.objects.create(user=self.user,company=self.company)
        #Create a client and login
        self.c = Client()

class RegisterCabinTestCase(DataCabinaTestCase):
    """
        Test cabin registering in the system using a token.
    """
    def setUp(self):
        super().setUp()
        self.c.login(username = 'test', password = 'test_password')
        #Create a cabin token
        self.token = CabinToken.objects.create()

    def test_register_new_cabin(self):
        """A cabin is registered correctly with an unused token"""
        response = self.c.post('/api/data/register_cabin/', {'token': self.token.id})
        content = response.json()
        self.assertEqual(content['detail'], 'successful')
        #self.assertEqual(self.token.is_used, True)
        print('Cabin registering...OK')

class CreateCaptureTestCase(DataCabinaTestCase):
    """
        Test captures registering
    """
    def setUp(self):
        super().setUp()
        #Create a cabin token
        self.token = CabinToken.objects.create()
        self.token.is_used = False
        self.token.save()
        #Create a cabins
        self.cabin = Cabin.objects.create(company=self.company, token = self.token)
        #Data
        self.data = {
                    'token': self.token.id,
                    'temp': random.uniform(36, 43),
                    'is_wearing_mask': random.uniform(0, 1) > 0.5,
                    'is_image_saved': True,
                    'image_base64' : self.create_image(),
        }

    def create_image(self, width=512, height=256):
        rgb_array = numpy.random.rand(int(height), int(width), 3) * 255
        image = Image.fromarray(rgb_array.astype('uint8')).convert('RGB')
        image_bytes = io.BytesIO()
        image.save(image_bytes, "JPEG")
        img_str = base64.b64encode(image_bytes.getvalue())
        return img_str

    def test_captures_data(self):
        """Test if data is correctly captured"""
        response = self.c.post('/api/data/captures_create/', self.data)        
        self.assertEqual(response.status_code, 200, response.content)
        content = json.loads(response.content)
        self.assertEqual(content['detail'], 'successful')
        print('Data capturing...OK')
