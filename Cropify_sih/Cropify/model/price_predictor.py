from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Embedding
import pickle, os, json
import numpy as np


class LogScaler:
    def __init__(self):
        self.scaler = MinMaxScaler()
    def fit(self,data):
        print("Fit Shape",data.shape)
        data = np.log(data)
        self.scaler.fit(data)
    def transform(self,data):
        data  = np.log(data)
        return self.scaler.transform(data)   
    def inverse_transform(self,data):
        data = self.scaler.inverse_transform(data)
        return np.exp(data)
    def fit_transform(self,data):
        self.fit(data)
        return self.transform(data)
    
class PriceConfig:
    def __init(self,time_lapse = 90):
        self.time_lapse = time_lapse
        self.columns

class PricePredictor:
    def __init__(self, model_name = 'v1'):
        self.price_scaler = LogScaler()
        if not os.path.exists("./price/" + model_name):
            os.makedirs("./price/" + model_name)   
        self.root_model_path = "./price/" + model_name        
        self.config = PriceConfig()
        
    def build_model(self,time_lapse):
        self.config.time_lapse = time_lapse
        model = Sequential()
        model.add(LSTM(70,return_sequences=True,input_shape = (15,self.config.time_lapse)))
        model.add(LSTM(70,return_sequences=True))
        model.add(Dropout(0.2))
        model.add(Dense(50))
        model.add(Dropout(0.2))
        model.add(Dense(40))
        model.add(Dropout(0.2))
        model.add(Dense(30))
        model.add(Dense(1))
        model.compile(optimizer='adam',loss='mae')
        self.model = model
        model.summary()
        
    def train(self,prices,epochs=20,train_split = 2000,columns = None):
        if columns is not None:
            self.config.columns = columns
        else:
            self.config.columns = prices.columns
            
        prices = self.price_scaler.fit_transform(prices)       
        X_train,y_train = self.preprocess(prices[:train_split])
        X_test,y_test = self.preprocess(prices[train_split:])
        self.model.fit(X_train,y_train,epochs = epochs,validation_data = (X_test,y_test))
        
    def save_model(self):
        self.model.save(os.path.join(self.root_model_path, "model.h5"))
        with open(os.path.join(self.root_model_path,"price_scaler.pkl"),"wb") as file:
            pickle.dump(self.price_scaler,file)
        with open(os.path.join(self.root_model_path,"config.pkl"),"wb") as file:
            pickle.dump(self.config,file)
            
    def load_model(self,model_root_path):
        from tensorflow.keras.models import load_model as ld
        self.model = ld(os.path.join(model_root_path, "model.h5"))
        print("2",model_root_path)
        with open(os.path.join(model_root_path,"price_scaler.pkl"),"rb") as file:
            self.price_scaler = pickle.load(file)
        with open(os.path.join(model_root_path,"config.pkl"),"rb") as file:
            self.config = pickle.load(file)
            
    def preprocess(self,prices):
        X = np.zeros((len(prices) - self.config.time_lapse-1,15,self.config.time_lapse))
        y = np.zeros((len(prices) - self.config.time_lapse-1,15))
        for i in range(self.config.time_lapse,len(prices)-1):
            #X[i-self.config.time_lapse,:] = list(zip(prices[i-self.config.time_lapse:i],temperature[i-self.config.time_lapse:i]))
            X[i-self.config.time_lapse,:] = prices[i-self.config.time_lapse:i,:].T
            y[i-self.config.time_lapse] = prices[i]
        return (X,y)
    
    def predict(self,prices):
        prices = self.price_scaler.transform(prices)       
        X,y = self.preprocess(prices)            
        predictions = self.model.predict(X)
        predictions = self.price_scaler.inverse_transform(np.squeeze(predictions,axis = -1))
        return predictions

if __name__ == "__main__":
    from sklearn.metrics import r2_score
    import pandas as pd
    from_index = -1000
    predictor = PricePredictor()
    predictor.load_model("./price/v1")
    augmented_df = pd.read_excel("./augmented_price_data.xlsx")
    for crop_index in range(15):
        predicted = predictor.predict(np.array(augmented_df)[from_index:])[:,crop_index]
        original = np.array(augmented_df)[from_index + predictor.config.time_lapse:][:-1,crop_index]        
        error = predicted - original
        print("Price Error: ",predictor.config.columns[crop_index],np.mean(error),"R^2",r2_score(original,predicted))