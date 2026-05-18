from django.db import models

# Create your models here.

class Usermodel(models.Model):
    username = models.CharField(max_length=20, null=True)
    first_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=10, null=True)
    password = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Usermodel'
