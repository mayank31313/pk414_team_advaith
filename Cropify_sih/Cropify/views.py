import json
from django.shortcuts import render
from django.db.models import Avg, Sum
from rest_framework import generics, permissions, viewsets, views
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import *
from django.contrib.auth import login
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from .models import *
from .model.recommender import Recommender, RecommenderEncoder
from .model.price_predictor import PricePredictor
import sys, random
import numpy as np
import pandas as pd
from datetime import date, timedelta

sys.path.append("./Cropify/model")

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
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
        print(self.predictor.config.columns)
        self.augmented_data = pd.read_excel("./Cropify/model/augmented_price_data.xlsx")

    def get(self,request,format=None):       
        crops = ['Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Cashew nut', 'Tea',
            'Coffee', 'Rubber', 'Wheat', 'Barley', 'Rape & Mustard', 'Maize',
            'Pulses', 'Jute', 'Jowar']

        responses = list()
        for crop in crops:
            data = PricesTable.objects.filter(price_date__gte = date.today(),crop=crop)
            response_data = dict()
            for crop_data in data:
                response_data[crop_data.price_date.strftime("%m/%d/%Y")] = crop_data.price

            responses.append([{
                "name": crop,
                "data": response_data
            }])
        return Response(responses)        

        
class userDetails(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get('username','')
        if username=='000000000000':
            return queryset
        else:
            return queryset.filter(username=username)

class ProductionApi(views.APIView):
    serlizer_class = ProductionSerializer
    def post(self,request,format=None):
        print(request.data)
        serializer=ProductionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data":"Submited Successfully"})

    def get(self,request):
        states = ProductionData.objects.order_by('state').values('state').distinct()
        response_data =  list()
        for state in states:
            query_set = ProductionData.objects.filter(state=state['state']).values('crop').annotate(avg_qnt=Sum('quantity'))
            print(query_set,state)
            response = dict()
            for production in query_set:
                response[production['crop']] = production['avg_qnt']
            response_data.append([{
                "name": state['state'],
                "data": response
            }])
        return Response(response_data)

class FailureApi(views.APIView):
    serlizer_class = FailureSerializer
    def post(self,request,format=None):
        serializer=FailureSerializer(data=request.data)        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "Report Submitted": True,
            "Token": "evshffgas-sdgfgbdhhf-" + str(random.randint(1000,2456))
        })
    
    def get(self,request):
        failures = FailureModel.objects.all()        
        response = list()
        for failure in failures:
            response.append({
                "crop" : failure.crop_name,
                "description" : failure.description,
                "area_affected" : failure.fail_area,
                "stage": failure.stages,
                "user" : {
                    "id":failure.user.pk,
                    "city": failure.user.city,
                    "name": failure.user.name,
                    "state": failure.user.state
                },
                "token": failure.unique_token,
                'approx_loss': failure.approx_loss
            })
        
        return Response(response)

class FarmModuleStart(views.APIView):
    def post(self,request):
        data = request.data
        land_area = data['land_area']
        crops = data['crops']
        soil_type = data['soil_type']
        resources = data['resources']
        state = data['state']
        water_resources = data['water_resources']


        query_set = CropsDays.objects.filter(crop_name__in = crops)
        response_list= list()
        for result_set in query_set:
            target_date = date.today() + timedelta(days=result_set.min_days_till_harvest)
            prices = PricesTable.objects.filter(price_date__gte = target_date, price_date__lte = target_date + timedelta(days=60),crop=result_set.crop_name).values('state','crop').annotate(avg_price = Avg('price'))           
            response = dict()
            for state_price in prices:
                query_set = ProductionData.objects.filter(
                    state=state_price['state'],
                    crop__in=crops).values('crop').annotate(avg_qnt=Sum('quantity')).order_by('avg_qnt')
                
                for data in query_set:
                    response[data['crop']] = data['avg_qnt']

            response_list.append({
                "name": state_price['state'],
                "data": response,
                #"days_to_harvest": CropsDays.objects.filter(crop_name=crop).values('min_days_till_harvest')[0]['min_days_till_harvest'],
                #"crop": crop,
                #"state": "MP",
                #"amt_harvesting": random.randint(3000,5000),
                #"estimated_profit": random.randint(3000,6000),
                #"irrigation": random.randint(500,1500)
            })
        return Response(response_list)    

class DistributerApi(views.APIView):
    def get(self,request):
        query_set = ProductionData.objects.order_by('state','crop').all()
        response_list = list()
        for r in query_set:
            response_list.append({
                "name": r.crop,
                "quantity": r.quantity,
                "farmer": {
                    "name": r.user.name,
                    "city": r.user.city,
                    "id": r.user.pk
                }
            })
        return Response(response_list)