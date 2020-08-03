from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import *

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'name', 'username','pincode','city','password','state','role')
    extra_kwargs = {
            'password': {'write_only': True}
        }
  def create(self, validated_data):
    user = User(
        name=validated_data['name'],
        username=validated_data['username'],
        pincode=validated_data['pincode'],
        city=validated_data['city'],
        state=validated_data['state'],
        role = validated_data['role']
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class CropSerializer(serializers.Serializer):
  class Meta:
    fields=("crops","soiltype","soilhealth")

class ProductionSerializer(serializers.ModelSerializer):
  class Meta:
    model=ProductionData
    fields=("crop","quantity","hector","user","state")

  def create(self, validated_data):
    production = ProductionData(
      crop = validated_data['crop'],
      quantity = validated_data['quantity'],
      hector= validated_data['hector'],
      user=validated_data['user'],
      state=validated_data['user'].state
    )
    u = validated_data['user']
    production.save()
    return production

class FailureSerializer(serializers.ModelSerializer):
  class Meta:
    model=FailureModel
    fields=("user","crop_name","fail_area","description","reason","land_area","stages","unique_token","approx_loss")