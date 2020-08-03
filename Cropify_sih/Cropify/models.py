from django.db import models
from django.contrib.auth.models import UserManager,AbstractBaseUser
from datetime import date
import django_mysql.models as mysql
import uuid

class User(AbstractBaseUser):
	name = models.CharField(max_length=20)
	username = models.CharField(max_length=12,unique=True)
	pincode = models.CharField(max_length=6)
	city = models.CharField(max_length=20)
	password = models.CharField(max_length=255)
	role = models.CharField(max_length=40,default="farmer")
	state = models.CharField(max_length=30,default=None)
	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

class ProductionData(models.Model):
	crop=models.CharField(max_length=15)
	quantity=models.IntegerField()
	hector=models.IntegerField()
	state = models.CharField(max_length=20,default=None)
	user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)


class PricesTable(models.Model):
	price_date = models.DateField(default=None)
	price = models.IntegerField()
	state = models.CharField(max_length=30)
	crop = models.CharField(max_length=20,default=None)

class FailureModel(models.Model):
	user = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
	description = models.CharField(max_length=255,default=None)
	reason = models.CharField(max_length=200)
	land_area = models.IntegerField()
	approx_loss = models.IntegerField(default=0)
	stages = models.IntegerField(default=0)
	unique_token = models.UUIDField(default=uuid.uuid4, editable=False)
	crop_name = models.CharField(default=None,max_length=20)
	fail_area = models.CharField(default=None,max_length=30)

class CropsDays(models.Model):
	crop_name = models.CharField(max_length=20)
	min_days_till_harvest = models.IntegerField()
	max_days_till_harvest = models.IntegerField()
"""
class FarmPlanModelForm(mysql.Model):
	land_area = models.IntegerField()
	crops = mysql.ListCharField(base_field=models.CharField(max_length=20),max_length=(20*16))
	soil_type = models.CharField(max_length=20)
	resources = models.CharField(max_length=255) 
"""

class FarmPlanModel(mysql.Model):
	days_to_harvest = models.IntegerField()
	crop = models.CharField(max_length=20)
	state = models.CharField(max_length=20)
	amount_harvest = models.IntegerField()
	estimated_profit = models.IntegerField()
	irrigation_required = models.IntegerField()
