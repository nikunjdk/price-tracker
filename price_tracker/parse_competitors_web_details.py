import logging
from bs4 import BeautifulSoup, Tag
from typing import Any

log = logging.getLogger("price_tracker.parse_competitors_web_details")


def parse_competitors_web_details(
    competitors_url: str, competitors_url_soup: BeautifulSoup
) -> list[Any]:
    """
    Parses competitor price data from a BeautifulSoup object representing a webpage.

    Args:
        competitors_url (str): The URL of the competitor's webpage.
        competitors_url_soup: A BeautifulSoup object containing the webpage content.

    Returns:
        List: A list of lists, where each inner list represents a row of competitor details.
              Each row contains relevant information such as product names and prices.

    Raises:
        Exception: If the competitor price table is not found or if no products are found.

    Example:
        >>> competitors_url = "https://example.com/competitors"
        >>> competitors_url_soup = BeautifulSoup(html_content, "html.parser")
        >>> parsed_details = parse_competitors_web_details(competitors_url, competitors_url_soup)
        >>> for row in parsed_details:
        ...     print(row)
        ['Product A', '100']
        ['Product B', '80']
        ...
    """
    try:
        # Extract competitor price table
        competitors_prices_table = competitors_url_soup.find(
            "div", attrs={"id": "sellers-table-wrap"}
        )
        if competitors_prices_table is None:
            log.error("'sellers-table-wrap' div not found")
            raise Exception(
                f"Competitor price table not found for url: {competitors_url}"
            )

        competitors_prices_table = competitors_prices_table.find("table")
        if competitors_prices_table is None:
            log.error("table not found")
            raise Exception(
                f"Competitor price table not found for url: {competitors_url}"
            )

        if not isinstance(competitors_prices_table, Tag):
            log.error("competitors_prices_table is not of type 'Tag'")
            raise Exception(
                f"Competitor price table not found for url: {competitors_url}"
            )
        else:
            # Remove unwanted divs
            for div in competitors_prices_table.find_all(
                "div", {"class": "seller-info-table"}
            ):
                div.decompose()

            # Extract table rows
            table_rows = competitors_prices_table.find_all("tr")
            parsed_competitors_details = []
            for tr in table_rows:
                td = tr.find_all("td")
                row = [tr.text.strip() for tr in td]
                if row:
                    parsed_competitors_details.append(row)
            return parsed_competitors_details
    except Exception:
        raise
