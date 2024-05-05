import petrosa

data = mongo.get_client()["petrosa_crypto"]["candles_h1"].find({"ticker": "BTCUSDT"}).sort("datetime", -1).limit(10)



print(data)