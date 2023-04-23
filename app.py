# %%
import requests
import pandas as pd
from datetime import datetime
import csv

etf50 = [row for row in csv.reader(open("data/0050.csv", "r", encoding="utf-8"))]
etf50_ids = [row[0] for row in etf50[1:]]

frames = []
for id in etf50_ids[:1]:
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
        "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
        "start_date": "2010-01-01",
        "data_id": id,
        "token": "",
    }

    data = requests.get(url, params=parameter)
    data = data.json()
    df = pd.DataFrame(data["data"])

    frames.append(df)

data = requests.get(url, params=parameter)
data = data.json()
data
