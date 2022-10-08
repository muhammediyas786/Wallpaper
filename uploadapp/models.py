from datetime import datetime
from email.policy import default
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=200, unique=True,default='')
    category_slug = models.SlugField(max_length=200, unique=True,default='iyas')
    def get_url(self):
        
        return reverse('category_slug',args=[self.category_slug])
    def __str__(self):
        return self.category_name
    def save(self, *args, **kwargs):
        self.category_slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)




class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    bio = models.TextField()
    profile_image = models.ImageField(upload_to='profile_img/', default='/static/assets/images/profile.jpg')
    

    def __str__(self):
        return self.firstname





class Wallpapers(models.Model):
    uid=models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='wallpapers')
    download_count = models.IntegerField(default=0)
    wallpappers_count=models.IntegerField(default=0)
    category=models.ManyToManyField(Category)
    date=models.DateTimeField(default=datetime.now, editable=False)
   

    def __str__(self):
        return self.name




class Downloaded(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Wallpapers, on_delete=models.CASCADE)
    date=models.DateTimeField(default=datetime.now, editable=False)
    count_of_downloads=models.IntegerField(default=1)
    
    def __str__(self):
        return self.image.name


class Downloadcount(models.Model):
    count_of_image_downloads=models.IntegerField(default=0)
    image = models.ForeignKey(Wallpapers, on_delete=models.CASCADE)
    def __str__(self):
        return self.image.name





class Uploadcount(models.Model):
    count_of_image_uploads=models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)