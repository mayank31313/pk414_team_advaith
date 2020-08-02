from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import User,ProductionData

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'name', 'username','pincode','city','password')
    extra_kwargs = {
            'password': {'write_only': True}
        }
  def create(self, validated_data):
    user = User(
        name=validated_data['name'],
        username=validated_data['username'],
        pincode=validated_data['pincode'],
        city=validated_data['city'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user

class CropSerializer(serializers.Serializer):
  class Meta:
    fields=("crops","soiltype","soilhealth")

class ProductionSerializer(serializers.Serializer):
  class Meta:
    model=ProductionData
    fields=("crop","quantity","hector","user")