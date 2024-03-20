import re
from bs4 import BeautifulSoup
import pandas as pd
import requests
import logging

from parse_competitors_web_details import parse_competitors_web_details


log = logging.getLogger("price-tracker.get_competitors_details")


def get_competitors_details(product_url: str) -> pd.DataFrame:
    try:
        # Modifying competitors url from product url
        competitors_url = re.sub(".html.*", "/all_sellers.html", product_url)

        # Sending request to competitors url
        competitors_url_response = requests.get(competitors_url)
        competitors_url_response.raise_for_status()

        # Parsing competitors webpage
        competitors_url_soup = BeautifulSoup(
            competitors_url_response.content, "html.parser"
        )
        parsed_competitors_details = parse_competitors_web_details(
            competitors_url, competitors_url_soup
        )

        # Create DataFrame with relevant columns
        columns = [
            "Sellers",
            "Offer Price",
            "Delivery Locations",
            "Quantity based Discount",
            "Quantity Available",
            "Min Quantity / Consignee",
            "Offer Product As",
            "Country of Origin",
        ]
        competitors_details = pd.DataFrame(parsed_competitors_details, columns=columns)
        if competitors_details.empty:
            log.error("dataframe is empty")
            raise Exception(
                f"Competitor price table not found for url: {competitors_url}"
            )
        return competitors_details
    except requests.exceptions.RequestException as e:
        log.error(f"Error fetching competitors data for url: {product_url}: {e}")
        raise
    except Exception as e:
        log.error(f"Error processing competitors data for url: {competitors_url}: {e}")
        raise
