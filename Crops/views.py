from django.shortcuts import render, HttpResponse
from django.contrib import messages
from datetime import timedelta, datetime
import joblib
from .models import Wheat
from .config import ACCOUNT_SID,AUTH_TOKEN,PHONE_NO
from twilio.rest import Client
from pandas import read_csv
from statsmodels.tsa.arima.model import ARIMA
import requests

def periodic_update(request):
    if request.method == 'POST':
        Uid_value = request.POST.get('Uid')
        Section_value = request.POST.get('Section')
        Temp_value = request.POST.get('Temp')
        Pressure_value = request.POST.get('Pressure')
        CO2_value = request.POST.get('CO2')
        Weight_value = request.POST.get('Weight')

        Items = Wheat.objects.filter(Uid=Uid_value,Section=Section_value)

        if Items.exists():
            for item in Items:
                item.Temp = Temp_value
                item.CO2 = CO2_value
                item.Pressure = Pressure_value
                item.Weight = Weight_value
                item.save()
        send_alert(Temp_value,Pressure_value,CO2_value)
    return HttpResponse("Stock updated")

def add_stock(request):
    if request.method == 'POST':
        Uid_value = request.POST.get('Uid')
        Section_value = request.POST.get('Section')
        Temp_value = request.POST.get('Temp')
        Pressure_value = request.POST.get('Pressure')
        CO2_value = request.POST.get('CO2')
        Weight_value = request.POST.get('Weight')
        Date_of_harvest_value = request.POST.get('Date_of_harvest')
        Date_of_harvest_value = datetime.strptime(Date_of_harvest_value, '%Y-%m-%d')
        Est_date_of_exp_value = timedelta(days=182) + Date_of_harvest_value

        new_record = Wheat.objects.create(
            Uid=Uid_value,
            Section=Section_value,
            Temp=Temp_value,
            Pressure=Pressure_value,
            CO2=CO2_value,
            Weight=Weight_value,
            Date_of_harvest=Date_of_harvest_value,
            Est_date_of_exp=Est_date_of_exp_value
        )
        send_alert(Temp_value,Pressure_value,CO2_value)
    return HttpResponse("Stock added")
    

def send_alert(Temp_value,Pressure_value,CO2_value):
    temperature_threshold = 50
    co2_threshold = 500
    pressure_threshold = 500
    if int(Temp_value) > temperature_threshold:
        api_url = 'http://127.0.0.1:8000/alert/'
        custom_message = 'Alert_Wheat_Temperature'
        phone_number = '8073855979'

        payload = {
            'custom_message': custom_message,
            'Phone': phone_number
        }

        try:
            response = requests.get(api_url, params=payload)
            print(f'API Response: {response.status_code} - {response.text}')

        except Exception as e:
            print(f'Error making API request: {e}')
    if int(Pressure_value) > pressure_threshold:
        api_url = 'http://127.0.0.1:8000/alert/'
        custom_message = 'Alert_Wheat_Pressure'
        phone_number = '8073855979'

        payload = {
            'custom_message': custom_message,
            'Phone': phone_number
        }

        try:
            response = requests.get(api_url, params=payload)
            print(f'API Response: {response.status_code} - {response.text}')

        except Exception as e:
            print(f'Error making API request: {e}')
    if int(CO2_value) > co2_threshold:
        api_url = 'http://127.0.0.1:8000/alert/'
        custom_message = 'Alert_Wheat_CO2_level'
        phone_number = '8073855979'

        payload = {
            'custom_message': custom_message,
            'Phone': phone_number
        }

        try:
            response = requests.get(api_url, params=payload)
            print(f'API Response: {response.status_code} - {response.text}')

        except Exception as e:
            print(f'Error making API request: {e}')

def alerts(request):
    custom_message = request.GET.get('custom_message', None)
    Phone = request.GET.get('Phone', None)

    if custom_message:
        account_sid = ACCOUNT_SID
        auth_token  = AUTH_TOKEN

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            to=f"+91{Phone}",
            from_=PHONE_NO,
            body=custom_message)
        return HttpResponse(custom_message)
    else:
        return HttpResponse("No Message in the alert!!")


        

def pred_price():
    series = read_csv('wheat_df-Update.csv', header=0, parse_dates=[0], index_col=0)
    series.index = series.index.to_period('D')
    model = ARIMA(series, order=(5, 1, 0))
    model_fit = model.fit()
    results = model_fit.forecast()
    return round(results[0], 2)


def home(request):
    registered_username = request.session.get('registered_username')
    price = pred_price()
    Items = Wheat.objects.filter(Uid=registered_username)
    return render(request, 'home.html', {'registered_username': registered_username,'Items':Items,'price':price})


