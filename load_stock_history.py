# %%
from __future__ import annotations

import requests
import pandas as pd
import datetime
from datetime import timedelta, datetime, date
import csv
from pathlib import Path


def latestCheck(x: str | date):
    if isinstance(x, str):
        x = datetime.strptime(x, "%Y-%m-%d").date()
    elif not isinstance(x, datetime.date):
        raise TypeError("x must be a string or a datetime.date object")

    today = date.today()

    if today == x:
        return True
    elif datetime.today().hour < 18 and (today - x) and (today - x).days <= 1:
        return True
    else:
        holiday_list = [
            date(2022, 7, 4),
            date(2023, 4, 24),
            date(2023, 4, 21),
            date(2023, 4, 20),
            date(2023, 4, 19),
            date(2023, 4, 18),
            date(2023, 4, 17),
        ]  # List of holiday dates
        if today.weekday() >= 5 or today in holiday_list:
            workday = today
            while workday.weekday() >= 5 or workday in holiday_list:
                workday -= timedelta(days=1)

            print(workday, x)

            if (workday - x).days < 0:
                raise Exception("Workday check failed: the workday is less than the data day.")
            elif (workday - x).days == 0:
                return True

        return False


# %%


latestCheck("2023-09-20")

# %%
stock_price_dir = "data/taiwan_stock_price"
etf50_filename = "data/0050.csv"

Path(stock_price_dir).mkdir(parents=True, exist_ok=True)


f = open("stderr.txt", "w")

etf50 = [row for row in csv.reader(open(etf50_filename, "r", encoding="utf-8"))]
etf50_ids = [row[0] for row in etf50[1:]]

frames = []
for id in etf50_ids[:2]:
    url = "https://api.finmindtrade.com/api/v4/data"
    parameters = {
        "dataset": "TaiwanStockPrice",
        "start_date": "2012-01-01",
        "data_id": id,
        "token": "",
    }

    response = requests.get(url, params=parameters)

    if response.ok:
        data = response.json()["data"]
    else:
        f.write(f"Failed to retrieve data for ID {id}\n")

    df = pd.DataFrame(data)
    df = df.loc[:, ["stock_id", "date"] + list(df.columns[2:])]
    df.to_csv(Path(stock_price_dir) / f"{id}.csv", index=False)

f.close()

# %%
data[-1]["date"]


# %%
response = requests.get(url, params=parameters)


# %%
