from flask import Flask, render_template, request, redirect, url_for
import requests
import random
import os

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY")
def get_weather_data(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()['weather'][0]['main']
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching weather for {city}: {e}")
        return "Unknown"

def get_mood(weather_condition):
    if weather_condition == "Rain":
        return "#4a4e59", "#ffffff", "YES", "Grab an umbrella or dissolve. Your choice."
    elif weather_condition == "Clear":
        return "#f9d71c", "#222222", "NO", "You have no excuse to stay inside. Go touch grass."
    elif weather_condition == "Snow":
        return "#eef5f8", "#222222", "NO", "But it is freezing. Stay inside."
    elif weather_condition == "Extreme":
        return "#8b0000", "#ffffff", "RUN", "I don't know what's happening out there, but you should probably hide."
    else:
        return "#a2c2e0", "#222222", "MAYBE", f"It's {weather_condition.lower()} outside. Just look out a window, I'm not a wizard."
@app.route('/', methods=['GET', 'POST'])
def index():
    city = "Bangalore"
    if request.method == 'POST':
        city = request.form.get('city', 'Bangalore')
    elif request.args.get('city'):
        city = request.args.get('city')

    weather_condition = get_weather_data(city)
    bg_color, text_color, main_answer, snark = get_mood(weather_condition)
    return render_template('index.html',
                           city=city,
                           weather=weather_condition,
                           bg_color=bg_color,
                           text_color=text_color,
                           main_answer=main_answer,
                           snark=snark)

@app.route('/roulette')
def roulette():
    extreme_cities = [
        "Yakutsk", "Death Valley", "London", "Cherrapunji",
        "Kuwait City", "Wellington", "Oymyakon", "Seattle"
    ]
    random_city = random.choice(extreme_cities)
    return redirect(url_for('index', city=random_city))

@app.route('/about')
def about():
    return render_template('about.html', bg_color="#111111", text_color="#f4f4f4")
if __name__ == '__main__':
    app.run(debug=True, port=5000)