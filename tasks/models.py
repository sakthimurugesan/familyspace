from django.db import models

class AddTask(models.Model):
    taskname=models.CharField(max_length=50)
    time=models.TimeField(default="00:00")
    date=models.DateField()
    towhom=models.CharField(max_length=50)
    desc=models.TextField(max_length=300)
    markasdone=models.BooleanField(default=False)
    