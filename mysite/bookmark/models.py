# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User)
    category= models.CharField(max_length=100)

    def __str__(self):
        return '%s %s'%(self.user,self.category)

class UserBookmark(models.Model):
    user = models.ForeignKey(User)
    bookmark = models.URLField()
    # tags = models.ManyToManyField('Tag',blank=True)
    tag = TaggableManager()
    
    def __str__(self):
        return '%i %s %s'%(self.id,self.user,self.bookmark)
        
# class Tag(models.Model):
#   name = models.CharField(max_length=100, unique=True)

# class UserBookmark(models.Model):
#     user = models.ForeignKey(User)
#     bookmark = models.URLField()
#     # tag = models.CharField(max_length = 100)
#     # tags = TaggableManager()
#     # tags = models.ManyToManyField('Tag',blank=True)
#     def __str__(self):
#         return '%i %s %s'%(self.id,self.user,self.bookmark)