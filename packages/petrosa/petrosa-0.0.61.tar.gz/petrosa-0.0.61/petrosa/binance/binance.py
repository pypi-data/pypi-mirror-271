import base64
import json
import logging
import os

import requests
import pkg_resources
import logging

ver = pkg_resources.get_distribution('petrosa').version
logging.info("petrosa-utils version: " + ver)



def get_future_assets():
    asset_list_raw = requests.get(
        'https://fapi.binance.com/fapi/v1/ticker/price').json()

    asset_list_full = []
    for item in asset_list_raw:
        if (item['symbol'][-4:] == 'USDT' or item['symbol'][-4:] == 'BUSD'):
            # print(item)
            asset_list_full.append(item["symbol"])

    return asset_list_raw

    
def build_request(ticker, type, price, stop_loss, take_profit, valid_until):
    token = f"{os.environ.get('BINANCE_API_KEY')};{os.environ.get('BINANCE_API_SECRET')}"

    price = float(price)
    stop_loss = float(stop_loss)
    take_profit = float(take_profit)

    data = {
        "token": token,
        "ticker": ticker,
        "type": type,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "strategy": "simple_gap_finder",
        "valid_until": valid_until
    }
    return data


def request_it(request) -> str:
    
    request = base64.b64encode(bytes(json.dumps(request), "utf-8"))
    request = request.decode()
    send_data ={"message": {"data": request}}
    send_data = json.dumps(send_data)
    
    
    logging.debug(send_data)
    
    resp = requests.post(
                            os.environ.get('BINANCE_ORDERS_ENDPOINT', ""), 
                            data=send_data
                            )
    
    logging.debug(resp.text)
    
    return resp.text
    
    
def send_order(ticker, type, price, stop_loss, take_profit, valid_until) -> str:
    req = build_request(ticker, type, price, stop_loss, take_profit, valid_until)
    ans = request_it(req)
    
    return ans