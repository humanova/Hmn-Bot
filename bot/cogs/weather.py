# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pyowm
from discord.ext import commands
import discord
from utils import confparser, strings

owm_icon_url_base = "http://openweathermap.org/img/w/"
mgm_url = "https://www.mgm.gov.tr/FTPDATA/analiz/sonSOA.xml"

class Weather(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        self.owm = pyowm.OWM(self.config.owm_token)
        self.timezone = 3 # utc+3 for turkey

    def get_owm_weather_data(self, place):
        raw_data = None
        try:
            raw_data = self.owm.weather_at_place(place)
        except:
            return None

        weather_data = raw_data.get_weather()

        wind_speed = weather_data.get_wind()['speed']
        humidity =  weather_data.get_humidity()
        temp = weather_data.get_temperature('celsius')['temp']
        icon_url = f"{owm_icon_url_base}{weather_data.get_weather_icon_name()}.png"
        # status = weather_data.get_status()
        # temp_max = weather.data.get_temperature('celsius').temp_max
        # temp_min = weather.data.get_temperature('celsius').temp_min
        # data_time = weather.get_reception_time(timeformat='iso')
        sunrise_hour = weather_data.get_sunrise_time('iso')[11:13]
        sunrise_min = weather_data.get_sunrise_time('iso')[14:16]
        sunset_hour = weather_data.get_sunset_time('iso')[11:13]
        sunset_min = weather_data.get_sunset_time('iso')[14:16]

        sunrise_str = f"{(int(sunrise_hour) + self.timezone) % 24}:{sunrise_min}"
        sunset_str = f"{(int(sunset_hour) + self.timezone) % 24}:{sunset_min}"

        return {'place': place,
                'temp': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'sunrise': sunrise_str,
                'sunset': sunset_str,
                'icon_url': icon_url}

    def get_mgm_weather_data(self, place):
        city_id = self.detect_city(place)
        if city_id is not None:
            data = urlopen(Request(mgm_url, headers={'User-Agent': 'Mozilla'})).read()
            parsed_data = BeautifulSoup(data, 'xml')
            weather_status = parsed_data.find_all('Durum')[city_id].get_text()
            # date = parse.find_all('PeryotBaslama')[0]
            # temp_max = parse.find_all('Mak')[city_id]
            # temp_min = parse.find_all('Min')[city_id]
            # period = parse.find_all('Peryot')[city_id]

            return {'place': place.upper(),
                    'status': weather_status}
        return None

    def detect_city(self, place):
        place = place.upper()
        if place in strings.mgm_city_map.keys():
            return strings.mgm_city_map[place]
        return None

    @commands.command(alias=['weather'])
    async def hava(self, ctx, *, place):
        """ Belirtilen konumdaki hava durumunu gönderir """

        owm_data = self.get_owm_weather_data(place)
        mgm_data = self.get_mgm_weather_data(place)

        if owm_data is not None:
            embed = discord.Embed(title=" ", color=0x00ffff)
            embed.set_thumbnail(url=owm_data['icon_url'])
            embed.add_field(name=":earth_africa: Yer", value=owm_data['place'], inline=True)
            embed.add_field(name=":thermometer: Sıcaklık", value=f"{owm_data['temp']}°C", inline=True)
            embed.add_field(name=":droplet: Nem", value=f"{owm_data['humidity']}%", inline=True)
            embed.add_field(name=":dash: Rüzgar Hızı", value=f"{owm_data['wind_speed']}m/s", inline=True)
            embed.add_field(name=":sunrise: Gün Doğumu", value=f"{owm_data['sunrise']} (utc+3)", inline=True)
            embed.add_field(name=":city_sunset: Gün Batımı", value=f"{owm_data['sunset']} (utc+3)", inline=True)

            if mgm_data is not None:
                embed.add_field(name="Durum :" , value=mgm_data['status'], inline=False)

            embed.set_footer(text="🔆 Kaynak : openweathermap.org ve mgm.gov.tr")
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Weather(bot))