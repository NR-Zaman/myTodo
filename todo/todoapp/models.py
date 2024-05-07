from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

STATUS_CHOICES = [
    ("Not Started","Not Started"),
    ("Running","Running"),
    ("Completed","Completed"),
]

class task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    taskname = models.CharField(max_length=1000)
    dadeline = models.DateTimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, null=False, blank=False,)
    details = models.CharField(max_length=1000)
    comment = models.CharField(max_length=1000)

    def __str__(self):
        return self.taskname
