import logging
from pandas import Series
from filter_competitors_details import filter_competitors_details
from get_competitors_details import get_competitors_details


def process_product(product: Series):
    try:
        log = logging.getLogger("price_tracker.process_product")
        log.debug(f"Processing product {product.name}: {product['URL']}")
        product_url = product["URL"]
        competitors_details = get_competitors_details(product_url)
        filtered_competitors_details = filter_competitors_details(
            competitors_details, delivery_locations=["TAMIL NADU", "All India"]
        )
        min_price = filtered_competitors_details["Final Price"].min()
        log.debug(f"Minimum price: {min_price}")
        return min_price
    except Exception as e:
        log.error(f"Error processing product ({product['URL']}): {e}", exc_info=True)
        return "NAN"
