import weather
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    data = weather.get_forecast()
    
    if data == 404:
        return render_template('404.html')
    return render_template('weather.html',weather=data[0],forecast_data=data[1],night=data[2])

