from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class client(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=100)
    age=models.IntegerField()
    place=models.CharField(max_length=100)




class Appointment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)   # track who booked
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    class Meta:
        unique_together = ('date', 'time') 

    def __str__(self):
        return f"{self.name} - {self.date} {self.time} ({self.status})"
