from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser

class User(AbstractBaseUser):
	name = models.CharField(max_length=20)
	username = models.CharField(max_length=10,unique=True)
	pincode = models.CharField(max_length=6)
	city = models.CharField(max_length=20)
	password = models.CharField(max_length=255)
	role = models.CharField(max_length=40)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

class ProductionData(models.Model):
	crop=models.CharField(max_length=15)
	quantity=models.CharField(max_length=10)
	hector=models.CharField(max_length=15)
	user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)