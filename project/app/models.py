from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class client(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    age=models.IntegerField()
    place=models.CharField(max_length=100)




