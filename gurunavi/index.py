# -*- coding: utf-8 -*-

import os
import json
import urllib.request
import logging
from os.path import join, dirname
from dotenv import load_dotenv

logging.basicConfig(filename='./log/logger.log', level=logging.DEBUG)
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
  logging.info(address)
  logging.info(freeword)
  shop_list = get_shop_list(address, freeword)
  list = json.loads(shop_list)["rest"]
  tmp_list = []
  for dic in list:
    tmp_list.append(dic.get("name"))
  if len(tmp_list) > 0:
    print(tmp_list[0])
  else:
    print("None")

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('function_name',
                        type=str,
                        help='set fuction name in this file')
    parser.add_argument('-i', '--func_args',
                        nargs='*',
                        help='args in function',
                        default=[])
    args = parser.parse_args()

    # このファイル内の関数を取得
    func_dict = {k: v for k, v in locals().items() if callable(v)}
    # 引数のうち，数値として解釈できる要素はfloatにcastする
    func_args = [float(x) if x.isnumeric() else x for x in args.func_args]
    # 関数実行
    ret = func_dict[args.function_name](*func_args)
