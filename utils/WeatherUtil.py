import requests


class WeatherUtil:
    KEY = '3b6a0e5fe4951642a14efca1cd956969'

    @staticmethod
    def get_weather(location):
        # 获取地理编码
        geo_url = f'https://restapi.amap.com/v3/geocode/geo?address={location}&key={WeatherUtil.KEY}'
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()

        # 从返回的JSON数据中提取城市代码
        city_code = geo_data['geocodes'][0]['adcode']

        # 使用城市代码获取天气信息
        weather_url = f'https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={WeatherUtil.KEY}'
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()['lives'][0]

        weather_info = f'weather:{weather_data["weather"]}, temperature:{weather_data["temperature"]}, winddirection:{weather_data["winddirection"]}, windpower:{weather_data["windpower"]}, reporttime:{weather_data["reporttime"]}'
        return weather_info
