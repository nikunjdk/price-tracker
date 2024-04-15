import logging
from typing import Any, List
from pandas import Series
from price_tracker.const import COLUMN_PRODUCT_URL
from price_tracker.filter_competitors_details import filter_competitors_details
from price_tracker.get_competitors_details import get_competitors_details


def get_min_competitor_price(product: Series) -> float:
    try:
        log = logging.getLogger("price_tracker.process_product")
        log.debug(f"Processing product {product.name}: {product['URL']}")
        product_url = product[COLUMN_PRODUCT_URL]
        competitors_details = get_competitors_details(product_url)
        filtered_competitors_details = filter_competitors_details(
            product, competitors_details
        )
        min_price = filtered_competitors_details["Final Price"].min()
        log.debug(f"Minimum price: {min_price}")
        return min_price
    except Exception as e:
        log.error(f"Error processing product ({product['URL']}): {e}", exc_info=True)
        return -1
