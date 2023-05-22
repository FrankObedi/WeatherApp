import math, time, datetime, requests, os
from flask import request

# get api key
key = os.getenv('SECRETE_KEY')

def get_day_time(date_time_txt,just_day=False):
    date_time = date_time_txt.split(' ')
    year, mon, day = (int(x) for x in date_time[0].split('-'))
    date_obj = datetime.date(year,mon,day)
    day = date_obj.strftime("%A")
        
    if just_day:
        return day
        
    time_24hr = date_time[1]
    t = time.strptime(time_24hr,"%H:%M")
    time_12hr = time.strftime("%I:%M %p", t)
    day_time = f"{day}, {time_12hr}"        
    return day_time

def is_night(hour):
    if hour >= 6 and hour < 18:
        return False
    return True

def get_forecast():
    # set a default city when website loads
    city = 'Toronto, Canada'        
    forecast_data = {}

    if request.method == 'POST':
        city = request.form.get('city')
    
    full_weather = 'http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=6&aqi=no&alerts=no'
    forecast = requests.get(full_weather.format('98f5dfe9505742899b1172054232003',city)).json()    
    
    
    #   check for 404 error
    if forecast.get("error") != None:
        return 404    
    else:
        print(forecast['location']['localtime'])
        hour = forecast['location']['localtime'].split(' ')[1].split(':')
        night = is_night(int(hour[0]))

        # single day weather data
        weather_data = {
        'city': f"{forecast['location']['name']}, {forecast['location']['country']}",
        'temp': int(forecast['current']["temp_c"]),
        'cond': forecast['current']["condition"]['text'],
        'feel': int(forecast['current']["feelslike_c"]),
        'icon': forecast['current']["condition"]['icon'],
        'date': get_day_time(forecast['location']['localtime']),
        }

        # five day weather data
        for i in range(1, len(forecast["forecast"]["forecastday"])):
            day = get_day_time(forecast["forecast"]["forecastday"][i]['date'],just_day=True)
            min_temp = forecast["forecast"]["forecastday"][i]['day']['mintemp_c']
            max_temp = forecast["forecast"]["forecastday"][i]['day']['maxtemp_c']
            icon = forecast["forecast"]["forecastday"][i]['day']['condition']['icon']
            data = {day: [math.floor(min_temp),math.floor(max_temp),icon]}
            forecast_data.update(data)
    print(forecast_data)
    return weather_data, forecast_data, night


    