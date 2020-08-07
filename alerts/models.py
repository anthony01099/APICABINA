from django.db import models
from django.contrib.auth.models import User
from api_cabina.models import BaseModel

# Create your models here.
class Alert(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.TextField(null=True, blank=True)
