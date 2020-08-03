from django.db import models
from api_cabina.models import *


class Company(BaseModel):
    """
        This is the company who is buying our service
    """
    name = models.CharField(max_length=20)
    description = models.TextField()
    users = models.ManyToManyField('auth.User')

class Cabin(BaseModel):
    """
        Cabins installed for a particular company
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    token = models.BigIntegerField(null=True)

class Capture(BaseModel):
    """
        Data captures for a particular cabin
    """
    cabin = models.ForeignKey('Cabin', on_delete=models.CASCADE, null=True)
    temp = models.FloatField()
    is_wearing_mask = models.BooleanField(default=False)
    is_image_saved = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True)

class Setting(BaseModel):
    """
        Settings for a company
    """
    company = models.ForeignKey('Company', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    save_images = models.BooleanField(default=False) #Specify if images should be saved from cabins
