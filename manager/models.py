from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=25)
    username = models.CharField(max_length=35)
    password = models.CharField(max_length=50)

    date_del = models.DateField(blank=True, null=True)