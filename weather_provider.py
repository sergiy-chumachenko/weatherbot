import requests
import logging

WEATHER_EMOJI = {"thunderstorm": u'\U0001F4A8',
                 "drizzle": u'\U0001F4A7',
                 "rain": u'\U00002614',
                 "snowflake": u'\U00002744',
                 "snowman": u'\U000026C4',
                 "atmosphere": u'\U0001F301',
                 "clearsky": u'\U00002600',
                 "fewclouds": u'\U000026C5',
                 "clouds": u'\U00002601',
                 "hot": u'\U0001F525',
                 "default": u'\U0001F300'
                 }


class OpenWeatherMapProvider:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, lon, lat):
        params = {
            'lon': lon,
            'lat': lat,
            'appid': self.api_key

        }
        response = requests.get(
            url=f'https://api.openweathermap.org/data/2.5/weather',
            params=params
        )
        return response.json()

    def parse_weather_data(self, data):
        try:
            weather = data['weather']
            temp = data['main']
            visibility = data['visibility']
            wind = data['wind']
        except (ValueError, TypeError) as e:
            logging.error('Unable to fetch weather data. %s', e)
        else:
            weather_desc = weather[0].get('description').replace(' ', '')
            emoji = WEATHER_EMOJI.get(weather_desc) \
                if weather_desc in WEATHER_EMOJI.keys() else WEATHER_EMOJI.get('default')
            wind_direction = self.get_direction(wind.get('deg'))
            weather_info = \
                f"\nWeather: {weather[0].get('main')} {emoji}\n" \
                    f"Temperature (AVG) -> {round(temp.get('temp') / 10, 2)}\n" \
                    f"Temperature (MIN) -> {round(temp.get('temp_min') / 10, 2)}\n" \
                    f"Temperature (MAX) -> {round(temp.get('temp_max') / 10, 2)}\n" \
                    f"Humidity -> {temp.get('humidity')}%\n" \
                    f"Pressure -> {temp.get('pressure')} hPa\n" \
                    f"Visibility -> {visibility / 1000} km\n" \
                    f"Wind speed -> {(wind.get('speed') / 1.6) * 60} km/h\n" \
                    f"Wind direction -> '{wind_direction}'"
            return weather_info

    @staticmethod
    def get_direction(degrees):
        compass_brackets = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
        if degrees < 0:
            return compass_brackets[round((360 + degrees) / 45)]
        else:
            return compass_brackets[round(degrees / 45)]
