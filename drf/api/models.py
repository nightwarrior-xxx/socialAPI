from django.db import models
from django.contrib.auth.models import User

import random
import os

def getFileName(filename):
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    return name, ext


def uploads(instance, filename):
    name, ext = getFileName(filename)
    newName = '{rand}{name}'.format(rand=random.randint(1, 1000000), name=name)
    return 'images/{user}/{newName}'.format(user=instance.user, newName=newName)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    city=models.CharField(max_length=50)
    country=models.CharField(max_length=25)
    zip = models.CharField(max_length=5)
    image = models.ImageField(upload_to='uploads', null=True, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def owner(self):
        return self.user