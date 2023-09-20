# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def scrape_holidays(year, country="taiwan"):
    """Scrape the website to get the holiday data for the given year.

    Args:
        year (int): The year to get the holiday data.
        country (str, optional): The country to get the holiday data. Defaults to "taiwan".

    Returns:
        pd.DataFrame: The DataFrame containing the holiday data.
    """

    url = "https://www.timeanddate.com/holidays/{}/{}".format(country, year)

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the table containing holiday data (you may need to inspect the webpage's HTML to find the right selector)
        holiday_table = soup.find("table", {"id": "holidays-table"})

        # Check if the table was found
        if holiday_table:
            data = []
            # Iterate through the rows of the table to extract holiday data
            for row in holiday_table.find_all("tr")[1:]:  # Skip the header row
                date_column = row.find_all("th")
                columns = row.find_all("td")
                if len(columns) >= 3:
                    date_str = date_column[0].text.strip()
                    date_obj = datetime.strptime(date_str, "%d %b").replace(year=year).date()
                    holiday_name = columns[1].text.strip()
                    holiday_type = columns[2].text.strip()
                    data.append([date_obj, holiday_name, holiday_type])

            # Create a DataFrame to store the holiday data
            df = pd.DataFrame(data, columns=["Date", "Holiday Name", "Type"])

            return df
        else:
            print("Holiday table not found on the page.")
            return None
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return None


if __name__ == "__main__":
    # Example usage with year 2023
    holiday_df = scrape_holidays(2023)
    print(holiday_df.head(10))
