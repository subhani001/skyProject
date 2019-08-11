from django.db import models
from rest_framework.viewsets import ModelViewSet


# Create your models here.
class Tasks(models.Model):
     id=models.IntegerField(primary_key=True)
     name=models.CharField(max_length=30)
     status=models.CharField(max_length=30)
     start_date=models.CharField(max_length=30)
     end_date=models.CharField(max_length=30)
     parent=models.IntegerField()
     duration=models.CharField(max_length=30)
     net_duration=models.CharField(max_length=30)
