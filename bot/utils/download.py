# 2020 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

# This file run as a subprocess and used by mrender cog
import sys
import requests

if __name__ == "__main__":
    url = sys.argv[1]
    path = sys.argv[2]
    try:
        f = requests.get(url, timeout=4.0, headers={'User-Agent': 'Hmn-Bot (https://humanova.github.io/hmnbot, 1.0)'})
        open(path, 'wb').write(f.content)
    except Exception as e:
        print(f"Couldn't download file : {url} : {e}")