from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=250, primary_key=True)
