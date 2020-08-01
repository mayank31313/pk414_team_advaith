import os, json, pickle
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import ast
import requests, datetime
import enum

def un_stack(data):
    l = list()
    for i in range(data.shape[1]):
        l.append(data[:,i])
    return l

def parse_data_frame(dataframe):
    X = np.zeros((len(dataframe),4))
    regresser_x = np.zeros((len(dataframe),4))
    
    X[:,0] = dataframe.State_Index.to_list()
    X[:,1] = dataframe.Soil_Index.to_list()
    X[:,2] = dataframe.Season_Index.to_list()
    X[:,3] = dataframe.Weather_Index.to_list()
    
    regresser_x = dataframe[["Noise N", "Noise OC","Noise P","Noise K"]]
    return X,np.array(regresser_x)

class Season(enum.Enum):
    KHARIF = 1
    WINTER = 2
    SUMMER = 3
    RAINY = 4
class Weather(enum.Enum):
    COLD = 1
    HOT = 2
    HUMID = 3

class WeatherAPI:
    API_KEY = "e46024399b538bcf3f625333391d3be4"
    ENDPOINT_URL = "http://api.openweathermap.org/data/2.5/weather"
    def call(self, lat, lng):
        parameters = {
            "lat": lat,
            "lon": lng,
            "appid": self.API_KEY
        }
        resp = requests.get(self.ENDPOINT_URL, params=parameters)
        data = resp.json()
        main_data = data['main']
        temperature = main_data['feels_like'] - 273.0
        humidity = main_data['humidity']

        hot_ness = temperature
        cold_ness = 100 - temperature
        total = hot_ness + cold_ness + humidity
        compute = np.array([hot_ness/total,cold_ness/total,humidity/total])
        index = np.argmax(compute)
        today = datetime.datetime.now()
        
        if today.month > 5 and today.month < 11:
            season = Season.KHARIF
        elif today.month == 12 or today.month == 1 or today.month == 2:
            season = Season.WINTER

        if index == 0:
            weather = Weather.HOT
        elif index == 1:
            weather = Weather.COLD
        else:
            weather = Weather.HUMID
        
        return (weather,season)
        
class RecommenderEncoder(json.JSONEncoder):
    def default(self, r):
        return r.__dict__
        
class Recommend:
    def __init__(self,confidence,crop_name):
        self.confidence = float(confidence)
        self.crop_name = crop_name
    def __str__(self):
        return json.dumps(self.__dict__)
    def __gt__(self, other):        
        return self.confidence > other.confidence

class Recommender():
    def __init__(self,model_dir = None,load_type = "train"):
        self.model_dir = model_dir
        self.meta_data = {}
        self.type = load_type
        self.weather = WeatherAPI()
        if model_dir is not None:
            if os.path.exists(model_dir):
                print("Found Model")               
                self.load_model(self.model_dir)
                if(load_type == "train"):
                    self.preprocess_data()
        else:
            self.soil_encoder = LabelEncoder()
            self.states_encoder = LabelEncoder()
            self.crops_encoder = LabelEncoder()
            self.season_encoder = LabelEncoder()
            self.weather_encoder = LabelEncoder()
            self.data_frame = pd.DataFrame()

            
    
    def build_model(self,output_neurons,summary = False):
        inputs = []
        input_vectors = []
        for i in range(self.X.shape[1]):
            input_x = tf.keras.Input((1,),name = "input_%d" % (i + 1))
            input_vector_x = tf.keras.layers.Embedding(int(np.max(self.X[:,i])) + 1,2)(input_x)
            inputs.append(input_x)
            input_vectors.append(input_vector_x)

        reg_input = tf.keras.Input((self.regression_input.shape[1],),name = "regr_input")
        inputs.append(reg_input)
        
        concat = tf.keras.layers.concatenate(input_vectors)
        concat = tf.keras.layers.Flatten()(concat)
        
        regr_dense = tf.keras.layers.Dense(4)(reg_input)
        concat = tf.keras.layers.concatenate([concat,regr_dense])
        
        hidden = tf.keras.layers.Dense(8,activation="tanh")(concat)
        hidden = tf.keras.layers.Dropout(0.5)(hidden)

        for i in range(2):
            hidden = tf.keras.layers.Dense(8 + 2 ** (i+1))(hidden)
            hidden = tf.keras.layers.Dropout(0.5)(hidden)

        outputs = list()
        for i in range(output_neurons[0]):
            output = tf.keras.layers.Dense(8,activation='relu')(hidden)
            outputs.append(tf.keras.layers.Dense(output_neurons[1],activation="softmax",name="output_%d"%(i + 1))(output))


        self.model = tf.keras.Model(inputs,outputs)
        if summary:
            self.model.summary()
        self.model.compile(optimizer="adam", loss="categorical_crossentropy",metrics=['acc'])
        self.meta_data['epochs'] = 0
    
    def transform(self,data_frame):
        df = data_frame.copy()
        
        df["Soil_Index"] = self.soil_encoder.transform(data_frame.Soil.to_list())
        df["State_Index"] = self.states_encoder.transform(data_frame.State.to_list())
        df["Crop_Index"] = self.crops_encoder.transform(data_frame.Crop.to_list())
        df["Season_Index"] = self.season_encoder.transform(data_frame.fs.to_list())
        df["Weather_Index"] = self.weather_encoder.transform(data_frame.fw.to_list())
        
        self.data_frame = df
        return df
        
    def fit_transform(self,data_frame):        
        self.soil_encoder.fit(data_frame.Soil.to_list())
        self.states_encoder.fit(data_frame.State.to_list())
        self.crops_encoder.fit(data_frame.Crop.to_list())
        self.season_encoder.fit(data_frame.fs.to_list())
        self.weather_encoder.fit(data_frame.fw.to_list())
        
        return self.transform(data_frame)

    def preprocess_data(self):
        df = self.data_frame
        self.X,self.regression_input = parse_data_frame(df)
        self.X_train = un_stack(self.X)
        self.y = np.zeros((len(df),2,len(df.Crop.unique())))
        for i, indexes in enumerate(df.Crop_Index.to_list()):
            for index,c in enumerate(indexes):
                self.y[i,index,c] = 1

        self.data_dict = [("regr_input",self.regression_input)]
        for i,x in enumerate(self.X_train):
            self.data_dict.append(("input_%d"%(i+1),x))
            
        self.data_dict = {key:value for key,value in self.data_dict}
        self.y = [self.y[:,i,:] for i in range(2)]
        
    def train(self,epochs = 100,steps_per_epoch = 10,clear = False):  
        for i in range(epochs):
            print(f"{i} Epoch of {epochs}")     
            history = self.model.fit(self.data_dict,self.y,epochs = steps_per_epoch)
            #self.meta_data[self.meta_data['epochs']] = history.history
            self.meta_data['epochs'] += 1
        
    def load_model(self,model_dir):
        self.model = tf.keras.models.load_model(os.path.join(model_dir,"model.h5"))
        #self.model.summary()
        self.soil_encoder = self.load_encoder(os.path.join(model_dir,"soil.pickle"))
        self.states_encoder = self.load_encoder(os.path.join(model_dir,"states.pickle"))
        self.crops_encoder = self.load_encoder(os.path.join(model_dir,"crops.pickle"))
        self.season_encoder = self.load_encoder(os.path.join(model_dir,"season.pickle"))
        self.weather_encoder = self.load_encoder(os.path.join(model_dir,"weather.pickle"))
        
        file = open(os.path.join(model_dir,"meta.json"),"r")
        self.meta_data = json.loads(file.read())
        file.close()
        if(self.type == "train"):
            self.data_frame = pd.read_excel(os.path.join(model_dir,"train_data.xlsx"),converters={"Crop_Index": ast.literal_eval})
        
    
    def predict(self,state,soil,lat,lng,deff):
        #fw,fs = self.weather.call(lat,lng)
        fw, fs = Weather.COLD, Season.RAINY
        fw,fs = fw.name.lower(),fs.name.lower()

        data = {
            "regr_input": np.asarray(deff),
            "input_1": self.states_encoder.transform(np.asarray([state]).reshape(-1,1)),
            "input_2": self.soil_encoder.transform(np.asarray([soil]).reshape(-1,1)),
            "input_3": self.season_encoder.transform(np.asarray([fs]).reshape(-1,1)),
            "input_4": self.weather_encoder.transform(np.asarray([fw]).reshape(-1,1)),
        }
        predictions = self.model.predict(data)
        output = dict()
        output['recommended'] = [
            Recommend(confidence = -1, crop_name = None),
            Recommend(confidence = -1, crop_name = None)
        ]
        output['recommendations'] = [Recommend(confidence = -1, crop_name = None)
                                        for _ in range(len(predictions[0][0]))]
        for index,prediction in enumerate(predictions):
            for i,score in enumerate(prediction[0]):
                crop_name = self.crops_encoder.inverse_transform([[i]])
                r = Recommend(confidence = score,crop_name=crop_name[0])
                if r > output['recommended'][index]:
                    output['recommended'][index] = r
                if r > output['recommendations'][i]:
                    output['recommendations'][i] = r

        return output
    
    def save_encoder(self,encoder,path):
        file = open(path,"wb")
        pickle.dump(encoder,file)
        file.close()
        
    def load_encoder(self,path):
        encoder = None
        with open(path, "rb") as input_file:
            encoder = pickle.load(input_file)
        return encoder
        
    def save_model(self,model_dir):
        if not os.path.exists(model_dir):
            os.mkdir(model_dir)
            
        self.save_encoder(self.states_encoder,os.path.join(model_dir,"states.pickle"))
        self.save_encoder(self.crops_encoder,os.path.join(model_dir,"crops.pickle"))
        self.save_encoder(self.soil_encoder,os.path.join(model_dir,"soil.pickle"))
        self.save_encoder(self.season_encoder,os.path.join(model_dir,"season.pickle"))
        self.save_encoder(self.weather_encoder,os.path.join(model_dir,"weather.pickle"))
        self.model.save(os.path.join(model_dir,"model.h5"))
        
        file = open(os.path.join(model_dir,"meta.json"),"w")
        file.write(json.dumps(self.meta_data))
        file.close()
        if(self.type == "train"):
            self.data_frame.to_excel(os.path.join(model_dir,"train_data.xlsx"))

if __name__ == "__main__":
    import argparse
    import pandas as pd
    import random
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--training-data', metavar='-t', type=str, nargs='+',default="train-data.xlsx",dest="data")
    parser.add_argument('--model', metavar='-m', type=str, nargs='+',default=None,dest = "m")
    parser.add_argument('--epochs', metavar='-e', type=int, nargs='+',default=1000,dest="epochs")
    
    args = vars(parser.parse_args())
    """
    system = Recommender(os.path.join("./","v1"))
    system.preprocess_data()
    """
    print(args)
    #train_df = pd.read_excel(args['data'])
    #system = Recommender()
    #system.fit_transform(train_df)
    #system.preprocess_data()
    #system.build_model(output_neurons=(1,train_df.Crop.unique().shape[0]),summary=True)
    #system.train(epochs=args['epochs'])
    #system.save_model(os.path.join("./","v5"))
    
    #print(system.model.evaluate(system.data_dict,system.y))
    system = Recommender(os.path.join("v5"),load_type="predict")
    test = pd.read_excel("./v5/train_data.xlsx").iloc[random.randint(0,30),1:] #Load Sample Test Data
    print(test)
    print("First Recommendation: %s, Second Recommedation: %s" % (test.Crop,test.SecondCrop))
    recommendations = system.predict(test.State,test.Soil,22.719568,75.857727,np.expand_dims(np.asarray(test[-9:-5]).astype(np.float32),0))
    print("*" * 10 + "Top Recommendations"  + "*" * 10)
    for recommendation in recommendations['recommended']:
        print(recommendation)
    print("*" * 10 + "Other Recommendations" + "*" * 10)
    for recommendation in recommendations['recommendations']:
        print(recommendation)