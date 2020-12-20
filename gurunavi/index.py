import os
import json
import urllib.request
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

# dotenvの設定
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

key = os.environ.get("GURUNAVI_API_KEY")

# APIキーの指定
url = "https://api.gnavi.co.jp/RestSearchAPI/v3/"

def get_shop_list(address, freeword):
  params = urllib.parse.urlencode({
    'keyid': key,
    'address': address,
    'freeword': freeword,
    'parking': 1,
    'lunch': 1,
  })
  response = urllib.request.urlopen(url + '?' + params)
  return response.read()

def return_first_shop_name(address, freeword):
  shop_list = get_shop_list(address, freeword)
  list = json.loads(shop_list)["rest"]
  tmp_list = []
  for dic in list:
    tmp_list.append(dic.get("name"))
  print(tmp_list[0])

