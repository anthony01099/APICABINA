from django.contrib.auth.models import User
from django.db import models

from api_cabina.models import BaseModel
from .utils import media_upload_to, generate_token
from django.conf import settings


class Company(BaseModel):
    """
        This is the company who is buying our service
    """
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name


class CabinToken(models.Model):
    """
        Provides tokens to uniquely register each cabin.
    """
    id = models.CharField(max_length=settings.CABIN_TOKEN_LENGTH, primary_key=True, default=generate_token, editable=False)
    is_used = models.BooleanField(default=False)


class Cabin(BaseModel):
    """
        Cabins installed for a particular company
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    token = models.ForeignKey('CabinToken', on_delete=models.CASCADE)
    wifi_ssid = models.CharField(max_length=100, null=True)
    wifi_password = models.CharField(max_length=100, null=True)
    language = models.CharField(max_length=5, default='en')


class Capture(BaseModel):
    """
        Data captures for a particular cabin
    """
    cabin = models.ForeignKey('Cabin', on_delete=models.CASCADE, null=True)
    temp = models.FloatField()
    is_wearing_mask = models.BooleanField(default=False)
    is_image_saved = models.BooleanField(default=False)
    image = models.FileField(upload_to=media_upload_to, null=True, blank=True)

    @property
    def image_base64(self):
        try:
            return self.image.read()
        except:
            return ''


class Setting(models.Model):
    """
        Settings for a company
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    save_all = models.BooleanField(default=False)  # Specify if images should be saved from cabins

    def __str__(self):
        return str(self.company) + " " + str(self.save_all)


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s - %s" % (str(self.company), str(self.user))
