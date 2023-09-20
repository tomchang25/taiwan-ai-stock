# %%
from bs4 import BeautifulSoup
import pandas as pd
import os


def scrape_etf50():
    """Scrape the website to get the stock data for the given year.

    Returns:
        pd.DataFrame: The DataFrame containing the stock data.
    """

    # Parser html, from: https://www.wantgoo.com/stock/etf/0050/constituent
    with open("data/0050.html", encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")

    # Locate the table by find the sibling html tag which have id attribute
    table = soup.find(id="holdingSeason").parent.find_next_sibling("table")

    stocks = []
    for row in table.find_all("tr")[4:]:
        # Extract the columns (td elements) from the current row
        columns = row.find_all("td")

        # Extract the stock id (first column)
        stock_id = columns[0].text.strip()

        # Extract the stock name (second column)
        stock_name = columns[1].text.strip()

        # Extract the stock ratio (third column)
        stock_ratio = columns[2].text.strip()

        stocks.append([stock_id, stock_name, stock_ratio])

    df = pd.DataFrame(stocks, columns=["id", "name", "ratio"])
    df.to_csv("data/0050.csv", index=False)

    return df


def load_etf50():
    """Load the stock data from the csv file.

    Returns:
        pd.DataFrame: The DataFrame containing the stock data.
    """
    if os.path.exists("data/0050.csv"):
        df = pd.read_csv("data/0050.csv")
    else:
        df = scrape_etf50()

    return df


if __name__ == "__main__":
    df = load_etf50()
    print(df.head(10))
