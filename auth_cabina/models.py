from django.db import models
from django.contrib.auth.models import User
from data_cabina.models import Company


# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "%s - %s" % (str(self.company), str(self.user))
