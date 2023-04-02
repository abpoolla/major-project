from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import face_recognition,base64
from django.shortcuts import render,redirect
User._meta.get_field('email')._unique = True

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics',unique=True)
    # cnp = models.CharField(max_length=13, default=settings.GLOBAL_SETTINGS.get('default_value'))
    # id_series = models.CharField(max_length=2, default=settings.GLOBAL_SETTINGS.get('default_value'))
    # id_number = models.CharField(max_length=6, default=settings.GLOBAL_SETTINGS.get('default_value'))
    # issued_by = models.CharField(max_length=20, default=settings.GLOBAL_SETTINGS.get('default_value'))
    address_1 = models.CharField(max_length=100, default=settings.GLOBAL_SETTINGS.get('default_value'))
    address_2 = models.CharField(max_length=100, default=settings.GLOBAL_SETTINGS.get('default_value'))
    aadharno=models.CharField(max_length=12,default=settings.GLOBAL_SETTINGS.get('default_value'),unique=True)

    city = models.CharField(max_length=20, default=settings.GLOBAL_SETTINGS.get('default_value'))
    county = models.CharField(max_length=30, default=settings.GLOBAL_SETTINGS.get('default_value'))
    postal_code = models.CharField(max_length=6, default=settings.GLOBAL_SETTINGS.get('default_value'))
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        
        
        img = Image.open(self.image.path)
        

        if img.height > 300 or img.width>300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            #img1.thumbnail(output_size)
            img.save(self.image.path)
            #img1.save(self.image1.path)
    
from django.db import models


# Create your models here.

# this model Stores the data of the Phones Verified
class phoneModel(models.Model):
    Mobile = models.IntegerField(blank=False)
    isVerified = models.BooleanField(blank=False, default=False)
    counter = models.IntegerField(default=0, blank=False)   # For HOTP Verification

    def __str__(self):
        return str(self.Mobile)