import json
from django.shortcuts import render
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, CropSerializer,ProductionSerializer
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import User
from .model.recommender import Recommender, RecommenderEncoder
from .model.price_predictor import PricePredictor
import sys
import numpy as np
import pandas as pd

sys.path.append("./Cropify/model")

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
         "token": AuthToken.objects.create(user)[1]
        })

# Login API
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        print(request.user)
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data   
        request.user = user['user']   
        return super(LoginAPI, self).post(request, format=None)

# Crop API
class CropApi(generics.GenericAPIView):
    serializer_class = CropSerializer
    def __init__(self):
        self.model = Recommender("Cropify/model/v5",load_type="predict")
    
    def post(self,request,format=None):
        print(request.data)
        serializer=CropSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        soil = request.data['soiltype']
        soilhealth = request.data['soilhealth']
        state = request.data['state']
        lat = request.data['latitude']
        lng = request.data['longitude']
        recommendations = self.model.predict(state,soil,lat,lng,np.array([[float(soilhealth['nitrogen']),float(soilhealth['organic_carbon']),float(soilhealth['phosphorous']),float(soilhealth['potassium'])]]))
        top_scoring = recommendations['recommended']
        return Response(json.loads(json.dumps(recommendations, cls = RecommenderEncoder)))

# Price API
class PriceApi(generics.ListAPIView):
    def __init__(self):
        self.predictor = PricePredictor()
        self.predictor.load_model("./Cropify/model/price/")
        self.augmented_data = pd.read_excel("./Cropify/model/augmented_price_data.xlsx")

    def get(self,request,format=None):
        time_frame = self.augmented_data.iloc[-242:,:]
        columns = self.predictor.config.columns        
        responses = list()
        for i in range(15):     
            predictions = self.predictor.predict(prices=np.array(time_frame))       
            for prediction in predictions:
                from datetime import date
                response = dict()
                response['unit'] = 'kg'
                response['factor'] = 1
                response['date'] = str(date.today())
                response['prices'] = dict(zip(columns,prediction))
                responses.append(response)
                self.augmented_data.append(pd.DataFrame(prediction))            
            time_frame = self.augmented_data.iloc[-242:,:]

        return Response(responses)        

        
class userDetails(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username','')
        if username=='0000000000':
            return queryset
        else:
            return queryset.filter(username=username)

class ProductionApi(generics.GenericAPIView):
    serlizer_class=ProductionSerializer
    def post(self,request,format=None):
        print(request.data)
        serializer=ProductionSerializer(data=request.data)
        serializer.user = request.query_params.get('user_id')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data":"Submited Successfully"})