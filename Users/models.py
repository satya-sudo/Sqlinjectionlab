from os import nice
from django.contrib.auth.models import AbstractUser

from django.db import models

# User model auth.

class User(AbstractUser):
    about = models.TextField(blank=True,null=True)
    score = models.IntegerField(default=0,null=True,blank=True)
    views = models.IntegerField(default=0,null=True,blank=True)
    salary = models.IntegerField(default=0,null=True,blank=True)



class Projects(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    link = models.URLField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=20,choices = (("private","private"),("public","public")),default="private")

    def __str__(self):
        return self.title


