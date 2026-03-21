from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_KEY = "c0938c98881f18a0d2d3ea0d39d58ced"

def get_weather_data(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        weather_main = data['weather'][0]['main']
        return weather_main
    except requests.exceptions.RequestException as e:
        print(f"API Error fetching weather for {city}: {e}")
        return "Unknown"

@app.route('/', methods=['GET', 'POST'])
def index():
    city = "Bangalore"
    if request.method == 'POST':
        city = request.form.get('city', 'Bangalore')

    weather_condition = get_weather_data(city)
    if weather_condition == "Rain":
        bg_color = "#4a4e59"
        text_color = "#ffffff"
        main_answer = "YES"
        snark = "Grab an umbrella or dissolve. Your choice."
    elif weather_condition == "Clear":
        bg_color = "#f9d71c"
        text_color = "#D3D3D3D"
        main_answer = "NO"
        snark = "But it is freezing. Stay inside."

    else:
        bg_color = "a2c2e0"
        text_color = "#D3D3D3D"
        main_answer = "MAYBE"
        snark = f"It's {weather_condition.lower()} outside. Just look out a window, I'm not a wizard."

    return render_template(
        'index.html',
        city=city,
        weather=weather_condition,
        bg_color=bg_color,
        text_color = text_color,
        main_answer=main_answer,
        snark=snark
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)