# %%
from bs4 import BeautifulSoup
import pandas as pd

# Parser html, from: https://www.wantgoo.com/stock/etf/0050/constituent
with open("data/0050.html", encoding="utf-8") as fp:
    soup = BeautifulSoup(fp, "html.parser")


# Locate the table by find the sibling html tag which have id attribute
first_table = soup.find(id="holdingSeason").parent.find_next_sibling("table")
stock_tag = first_table.find_all("td")

stocks = []
for i in range(0, len(stock_tag), 8):
    stock_id = stock_tag[i].text.strip()
    stock_name = stock_tag[i + 1].text.strip()
    stock_ratio = stock_tag[i + 2].text.strip()

    stocks.append([stock_id, stock_name, stock_ratio])

df = pd.DataFrame(stocks, columns=["id", "name", "ratio"])
df.to_csv("data/0050.csv", index=False)
with open("data/0050.json", "w") as f:
    f.write(df.to_json(orient="records"))
