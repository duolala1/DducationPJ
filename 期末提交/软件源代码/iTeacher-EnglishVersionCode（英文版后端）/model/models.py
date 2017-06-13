from __future__ import unicode_literals

from django.db import models

# Create your models here.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Test(models.Model):
    name = models.CharField(max_length=20)
class bookInfo(models.Model):
	bookID = models.CharField(max_length=50)
	bookName = models.CharField(max_length=300)
	bookDetail = models.CharField(max_length=3000)
	imgUrl = models.CharField(max_length=500)
	author = models.CharField(max_length=100)

class labels(models.Model):
	bookID = models.CharField(max_length=50)
	label = models.CharField(max_length=200)

class user(models.Model):
	userName = models.CharField(max_length=50)
	userPasswd = models.CharField(max_length=50)
class Preference(models.Model):
	userName = models.CharField(max_length=50)
	comments = models.CharField(max_length=500)
	bookID = models.CharField(max_length=50)
class scores(models.Model):
	userName = models.CharField(max_length=50)
	score = models.CharField(max_length=3)
	bookID = models.CharField(max_length=50)