from fastapi import FastAPI, Request, Form, Depends
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
from requests import request
import sklearn
import numpy as np


class Features(BaseModel):
    Year: int
    Present_Price: int
    Kms_Driven: int
    Fuel_Type_Petrol: str
    Owner: int
    Seller_Type_Individual: str
    Transmission_Mannual: str

    @classmethod
    def as_form(
        cls,
        Year: int = Form(...),
        Present_Price: int = Form(...),
        Kms_Driven: int = Form(...),
        Fuel_Type_Petrol: str = Form(...),
        Owner: int = Form(...),
        Seller_Type_Individual: str = Form(...),
        Transmission_Mannual: str = Form(...)


    ):
        return cls(Year = Year,  Present_Price= Present_Price, Kms_Driven=Kms_Driven, Fuel_Type_Petrol=Fuel_Type_Petrol, Owner=Owner, Seller_Type_Individual=Seller_Type_Individual, Transmission_Mannual=Transmission_Mannual)





app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates/')

model = pickle.load(open('models/random_forest_regressor_model.pkl', 'rb'))


@app.get("/")
def read_item(request: Request, response_class = HTMLResponse):
    return templates.TemplateResponse('index.html', {"request":request, 'prediction_text': 'prediction result'})


@app.post("/predict", response_class=HTMLResponse)
def prediction(request: Request, form_data: Features = Depends(Features.as_form)):
    #print(dict(form_data))
    feature = dict(form_data)
    #print(feature, feature.keys())
    Fuel_Type_Diesel = 0
    Year = feature['Year']
    Present_Price = feature['Present_Price']
    Owner = feature['Owner']
    Kms_Driven = feature['Kms_Driven']
    Fuel_Type_Petrol = feature['Fuel_Type_Petrol'] 
    Seller_Type_Individual = feature['Seller_Type_Individual']
    Transmission_Mannual = feature['Transmission_Mannual']

    if(Fuel_Type_Petrol=='Petrol'):
        Fuel_Type_Petrol=1
        Fuel_Type_Diesel=0
    elif(Fuel_Type_Petrol=='Diesel'):
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=1
    else:
        Fuel_Type_Petrol=0
        Fuel_Type_Diesel=0
    Year=2020-Year
    if(Seller_Type_Individual=='Individual'):
        Seller_Type_Individual=1
    else:
        Seller_Type_Individual=0	
    
    if(Transmission_Mannual=='Mannual'):
        Transmission_Mannual=1
    else:
        Transmission_Mannual=0
    prediction=model.predict([[Present_Price,Kms_Driven,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Mannual]])
    output=round(prediction[0],2)
    if output < 0:
        return templates.TemplateResponse('index.html', {"request":request, 'prediction_text': "You cannot sell this car"})

    else:
        return templates.TemplateResponse('index.html', {"request":request, 'prediction_text': f"your car price is {output} lakh"})




    
    
