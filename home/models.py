from django.db import models
from django.utils import timezone

class user(models.Model):
    username=models.CharField(max_length=50,primary_key=True)
    password=models.TextField()
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    email=models.EmailField()
    address=models.TextField(default='')
    timestamp=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.username


class price_calculate(models.Model):
    weight=models.FloatField()
    price=models.IntegerField()

class order(models.Model):
    cake_name=models.CharField(max_length=50)
    weight=models.FloatField()
    username=models.CharField(max_length=50)
    delivered_status=models.BooleanField(default=False)
    timestamp=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return str(self.id)+") "+str(self.cake_name)+" by "+str(self.username)


class feedback(models.Model):
    username=models.CharField(max_length=50)
    text=models.TextField()
    timestamp=models.DateTimeField(default=timezone.now())
    def __str__(self):
        return self.username


class cake(models.Model):
    cake_name=models.CharField(max_length=90,primary_key=True)


