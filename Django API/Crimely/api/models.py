from django.db import models
import os
# Create your models here.


def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return os.path.join('uploads', filename)


class DocModel(models.Model):
    stoken = models.CharField(max_length=50, unique=False, default='')
    date = models.DateTimeField(auto_now_add=True)
    vid = models.FileField(upload_to='documents/')

    def __str__(self):
        return str(self.date)
    
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length = 50)
    email = models.EmailField()
    Pass = models.CharField(max_length = 20)
    confpass = models.CharField(max_length = 20)

    def __str__(self) -> str:
        return self.fullname

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    property_name = models.CharField(max_length = 100)
    property_address = models.TextField()
    User = models.ForeignKey(Users, on_delete = models.CASCADE)
