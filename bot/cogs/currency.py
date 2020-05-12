# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

# data sources :
#          !doviz : canlidoviz.com
#          !kripto : coinmarketcap.com

import locale
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests
import json
from utils import confparser, pasta, strings

currency_api_url = "https://api.canlidoviz.com/items/latest-data?marketId=0&type=CURRENCY"
gold_api_url = "https://api.canlidoviz.com/items/latest-data?marketId=0&type=GOLD"
crypto_graph_base_url = "https://s2.coinmarketcap.com/generated/sparklines/web/7d/usd/"


class Currency(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = confparser.get("config.json")
        locale.setlocale(locale.LC_ALL, 'en_US.UTF8')

    def parse_currency(self, currency, count=1, is_detailed=False):
        currency_code = self.detect_currency(currency)
        if currency_code is not None and float(count) > 0 and count is not None:

            if currency_code == "ALTIN":
                currency_data = self.get_gold()

            elif currency_code == "OSU":
                months = count
                count = float(months) * 4.0
                currency_name = "AYLIK SUPPORTER"
                data = self.get_currency("USD", count)
                currency_data = {"currency_name": currency_name,
                                 "currency_buy": data['currency_buy'],
                                 "currency_change": data['currency_change'],
                                 "discount": self.calculate_supporter_discount(months, data['currency_buy']),
                                 "currency_time": data['currency_time']}

            elif currency_code == "NITRO":
                count = float(count) * 5.0
                currency_name = "AYLIK NITRO"
                data = self.get_currency("USD", count)
                currency_data = {"currency_name": currency_name,
                                 "currency_buy": data['currency_buy'],
                                 "currency_change": data['currency_change'],
                                 "currency_time": data['currency_time']}

            else:
                if is_detailed:
                    currency_data = self.get_currency_detailed(currency_code)
                else:
                    currency_data = self.get_currency(currency_code, count)

            return currency_data

        else:
            return None

    def parse_crypto(self, currency, count=1):
        if currency is not None and count is not None:
            currency_code, graph_url = self.detect_crypto(currency)

            if currency_code is not None and float(count) > 0:

                currency_url = 'https://coinmarketcap.com/currencies/' + currency_code

                data = urlopen(Request(currency_url, headers={'User-Agent': 'Mozilla'})).read()
                parse = BeautifulSoup(data, 'html.parser')

                k_delta = parse.find("span", "cmc--change-positive cmc-details-panel-price__price-change")

                if k_delta is None:
                    k_delta = parse.find("span", "cmc--change-negative cmc-details-panel-price__price-change")

                crypto_price_parse = parse.find("span", "cmc-details-panel-price__price").text
                crypto_price = locale.atof(crypto_price_parse.strip("$"))

                currency_price = round(crypto_price, 2)
                currency_delta = k_delta.text

                return {"currency_name": currency_code.upper(),
                        "currency_price": currency_price * count,
                        "currency_change_percentage": currency_delta[2:-3],
                        "currency_graph": graph_url}

        else:
            return None

    def detect_currency(self, currency):
        if currency is None:
            return None
        else:
            try:
                val_arr = strings.currency_map.values()
                for val in val_arr:
                    if currency in val:
                        return val[0]
                return None
            except:
                pass

    def detect_crypto(self, currency):
        if currency is None:
            return None
        else:
            aliases = []
            for v in strings.crypto_currency_map.values():
                aliases.append(v['aliases'])
            for val in aliases:
                if currency in val:
                    curr = strings.crypto_currency_map[val[0].lower()]
                    currency_name = curr['currency']
                    currency_graph_url = f"{crypto_graph_base_url}{curr['graph_id']}.png"

                    return currency_name, currency_graph_url
            return None

    def get_currency(self, currency, count):
        r = requests.get(currency_api_url, timeout=2)
        if r.status_code == 200:
            data = r.json()
            for i in data:
                if i['code'] == currency:
                    currency_buy = round(float(i['data']['lastBuyPrice']), 5)
                    currency_change = round(float(i['data']['dailyChange']), 5)
                    currency_change_percentage = round(float(i['data']['dailyChangePercentage']), 5)
                    currency_time = i['data']['lastUpdateDate']

                    return {"currency_name": currency,
                            "currency_buy": currency_buy * count,
                            "currency_change": currency_change,
                            "currency_change_percentage": currency_change_percentage,
                            "currency_time": currency_time}
                else:
                    continue
        return None

    def get_currency_detailed(self, currency):
        r = requests.get(currency_api_url, timeout=2)
        if r.status_code == 200:
            data = r.json()
            for i in data:
                if i['code'] == currency:
                    currency_min = float(i['data']['todayLowestSellPrice'])
                    currency_max = float(i['data']['todayHighestSellPrice'])
                    currency_buy = float(i['data']['lastBuyPrice'])
                    currency_sell = float(i['data']['lastSellPrice'])
                    currency_change = float(i['data']['dailyChange'])
                    currency_change_percentage = float(i['data']['dailyChangePercentage'])
                    currency_time = i['data']['lastUpdateDate']

                    return {"currency_name": currency,
                            "currency_min": currency_min, "currency_max": currency_max,
                            "currency_buy": currency_buy, "currency_sell": currency_sell,
                            "currency_change": currency_change, "currency_change_percentage": currency_change_percentage,
                            "currency_time": currency_time}
                else:
                    continue
        return None

    def get_gold(self):
        gold_data = dict()
        gold_data['currency_name'] = "ALTIN"
        r = requests.get(gold_api_url, timeout=2, headers={"User-Agent": "curl/7.61.0"})

        if r.status_code == 200:
            data = r.json()
            gold_data['currency_time'] = data[0]['data']['lastUpdateDate']

            for i in range(len(data)):
                if i < 5 or (i > 10 and i < 13):
                    gold_data[data[i]['name']] = float(round(data[i]['data']['lastBuyPrice'], 5))

            if not len(gold_data) == 0:
                return gold_data
            else:
                return None

        return None

    def calculate_supporter_discount(self, months, price):
        months = float(months)
        price = float(price)

        if months < 4.0:
            discount_price = price
        elif 4.0 <= months < 6:
            discount_price = price - (price * 0.25)
        elif 6.0 <= months < 8:
            discount_price = price - (price * 0.33)
        elif 8.0 <= months < 9:
            discount_price = price - (price * 0.38)
        elif 9.0 <= months < 10:
            discount_price = price - (price * 0.39)
        elif 10.0 <= months < 12.0:
            discount_price = price - (price * 0.40)
        elif months >= 12:
            discount_price = price - (price * 0.46)

        discount_price = round(float(discount_price), 3)
        return str(discount_price)

    def get_embed_color(self, currency):
        if currency == "AYLIK SUPPORTER":
            return 0xef6ca6
        elif currency == "AYLIK NITRO":
            return 0x80a7ff
        elif currency == "ALTIN":
            return 0xefed3a
        else:
            return 0x73b5ff

    @commands.command()
    async def doviz(self, ctx, curr:str, count:int=1):
        """ Belirtilen kur bilgisini gönderir """
        curr_data = self.parse_currency(curr.upper(), count, is_detailed=False)
        if curr_data is not None:

            embed = discord.Embed(title=" ", color=self.get_embed_color(curr_data['currency_name']))
            embed.set_author(name="Döviz Kurları", icon_url=ctx.bot.user.avatar_url)
            embed.set_footer(text=f"💰 Kaynak : canlidoviz.com | {curr_data['currency_time']}")

            if not curr_data['currency_name'] == "ALTIN":
                embed.add_field(name=f"{count} {curr_data['currency_name']}/TL", value=curr_data['currency_buy'], inline=True)
                embed.add_field(name="Günlük Değişim", value=curr_data['currency_change'],
                                inline=True)

            if curr_data['currency_name'] == "AYLIK SUPPORTER":
                embed.add_field(name="Indirimli", value=f"~{curr_data['discount']}", inline=False)

            elif curr_data['currency_name'] == "ALTIN":
                for i in range(len(curr_data) - 2):
                    gold_name = list(curr_data)[i + 2]
                    gold_price = curr_data[list(curr_data)[i + 2]]
                    embed.add_field(name=gold_name, value=f"{gold_price}", inline=False)

            await ctx.send(embed=embed)

    @commands.command()
    async def xdoviz(self, ctx, curr: str):
        """ Belirtilen kur bilgisini gönderir (detaylı) """
        curr_data = self.parse_currency(curr.upper(), is_detailed=True)
        if curr_data is not None:
            await ctx.send(f"```json\n{json.dumps(curr_data, indent = 4)}```")

    @commands.command(aliases=['crypto'])
    async def kripto(self, ctx, currency_code: str, count:int = 1):
        """ Belirtilen kripto kur bilgisini gönderir """
        curr_data = self.parse_crypto(currency_code.upper(), count=count)
        if curr_data is not None:

            usd_data = self.parse_currency(currency='USD')

            curr_name = curr_data['currency_name']
            curr_price = curr_data['currency_price']
            curr_change = curr_data['currency_change_percentage']
            curr_graph = curr_data['currency_graph']

            curr_price = round(curr_price, 2)
            price_tl = round(usd_data['currency_buy'] * curr_price, 2)
            embed = discord.Embed(title=" ", color=0xf7931a)
            embed.set_author(name=f"Kripto Kurları [{curr_name}]", icon_url=ctx.bot.user.avatar_url)
            embed.add_field(name=f"{count} {curr_name} / USD", value=curr_price, inline=True)
            embed.add_field(name=f"{count} {curr_name} / TRY", value=price_tl, inline=True)

            if not str(curr_change).startswith("-"):
                embed.add_field(name="Günlük Değişim", value=":arrow_up_small: " + str(curr_change) + "%", inline=True)
            else:
                embed.add_field(name="Günlük Değişim", value=":arrow_down_small: " + str(curr_change) + "%",
                                inline=True)

            embed.add_field(name="Son 7 günlük grafik", value=strings.komut["kripto-cizgi"], inline=True)
            embed.set_image(url=curr_graph)
            embed.set_footer(text="💎 Kaynak : coinmarketcap.com")

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Currency(bot))

