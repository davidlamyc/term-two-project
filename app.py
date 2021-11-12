# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:40:41 2020

@author: win10
"""

# 1. Library imports
import uvicorn
from fastapi import FastAPI
from Attributes import Attribute
import numpy as np
import pickle
import pandas as pd
# 2. Create the app object
app = FastAPI()
pickle_in = open("classifier.pkl","rb")
classifier=pickle.load(pickle_in)

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    return {'message': 'Hello, World'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To The App': f'{name}'}

# 3. Expose the prediction functionality, make a prediction from the passed
#    JSON data and return the predicted days
@app.post('/predict')
def predict(data:Attribute):
    data = data.dict()
    customer_seller_distance=data['customer_seller_distance']
    freight_value=data['freight_value']

   # print(classifier.predict([[variance,skewness,curtosis,entropy]]))
    prediction = classifier.predict([[customer_seller_distance,freight_value]])

    return {
        'prediction': prediction[0]
    }

# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8000
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
    
#uvicorn app:app --reload