from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10,blank=True,null=True)
    national_code = models.CharField(max_length=10,blank=True,null=True)
    num_homes = models.PositiveSmallIntegerField(default=0)
    about = models.TextField(default='asdasd')
    def get_absolute_url(self):
        return "/persons/users/%s/" %self.user.pk
    def __str__(self):
        return str((self.user))
class Home(models.Model):
    name = models.CharField(max_length=30,blank=True,null=True)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    address = models.TextField(default='abc')
    about = models.TextField(default='abc')
    zip_code = models.CharField(max_length=10,default='123')
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    member = models.ForeignKey(User,related_name="homes")


    def __str__(self):
    	return str((self.pk))
    def get_absolute_url(self):
        return "/persons/home/%s/" %self.pk
class Picture(models.Model):
    homeid = models.ForeignKey(Home)
    image = models.URLField(upload_to='persons')
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    def __str__(self):
        return (str(self.pk))
    # def get_absolute_url(self):
    #     return reverse("persons:detail_home", kwargs={"id": self.homeid})
    def get_absolute_url(self):
        return "/persons/home/%s/" %self.homeid

class State(models.Model):
    name = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return (str(self.name))
class City(models.Model):
    ostan = models.ForeignKey(State)
    name = models.CharField(max_length=30,unique=True)
    def __str__(self):
        return (str(self.name))


# comments
class Comment(models.Model):
    home = models.ForeignKey(Home)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextUploadingField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    def __str__(self):
        return (str(self.text))


class TrueFalseQuestion(models.Model):
    question = models.CharField(max_length=200,)
    answer = models.BooleanField(default=False)
    home = models.ForeignKey(Home,on_delete=models.CASCADE,default="1")
    def __str__(self):
        return (str(self.question))



    