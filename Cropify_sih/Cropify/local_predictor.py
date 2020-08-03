from .model.price_predictor import PricePredictor
from datetime import date , timedelta
from .models import *
import pandas as pd
import numpy as np
import sys, random

sys.path.append("./Cropify/model")

def save_predictions_to_db(days):
    predictor = PricePredictor()
    predictor.load_model("./Cropify/model/price/")
    augmented_data = pd.read_excel("./Cropify/model/augmented_price_data.xlsx")
    columns = predictor.config.columns
    time_frame = augmented_data.iloc[-242:,:]
    for j in range(days):       
        predictions = predictor.predict(prices=np.array(time_frame))       
        for i,prediction in enumerate(predictions[0]):         
            prices = PricesTable(crop=columns[i],state="MP",price_date=date.today() + timedelta(days=j + 30),price=prediction)
            prices.save()

        predictions = predictor.predict(prices=np.array(time_frame))       
        d = dict(zip(columns,np.reshape(predictions[0],(-1,1))))
        time_frame = time_frame.append(pd.DataFrame(d)).iloc[-242:,:]

def create_dummy_production(values = 50):
    states = ["MP","Bihar"]
    crops = ['Sugarcane', 'Cotton', 'Tobacco', 'Paddy', 'Cashew nut', 'Tea',
       'Coffee', 'Rubber', 'Wheat', 'Barley', 'Rape & Mustard', 'Maize',
       'Pulses', 'Jute', 'Jowar']

    users = User.objects.all()

    for state in states:
        for v in range(values):
            user = users[random.randint(0,len(users)-1)]
            production = ProductionData(state=user.state,crop=crops[random.randint(0,len(crops)-1)],quantity=random.randint(300,600),hector=random.randint(400,700),user=user)
            production.save()

def create_dummy_crop_days():
    crops = [('Sugarcane',300,540), ('Cotton',42, 50), ('Tobacco',70,130), ('Paddy',90,110), ('Cashew nut',1080,3600),('Tea',40,50),
       ('Coffee',60,90), ('Rubber',180,270), ('Wheat',130,171), ('Barley',65,70), ('Rape & Mustard',90,95), ('Maize',40,50),
       ('Pulses',40,60), ('Jute',120,150), ('Jowar',65,75)]

    for crop,min_, max_ in crops:
        c = CropsDays(crop_name=crop,min_days_till_harvest=min_,max_days_till_harvest=max_)
        c.save()

    