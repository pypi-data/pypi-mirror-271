import pandas as pd

from petrosa.checkers import consistency
from petrosa.database import mongo

data = mongo.get_client()["petrosa_crypto"]["candles_h1"].find({"ticker": "BTCUSDT"}).sort("datetime", -1).limit(1010)

df = pd.DataFrame(list(data))

const = consistency.check_consistency(start=min(df["datetime"]), 
                                      end=max(df["datetime"]), 
                                      actual=df["datetime"],
                                      period="h1"
                                      )
print(const)