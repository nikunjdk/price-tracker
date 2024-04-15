import logging
from typing import Any
import pandas as pd

from price_tracker.calculate_minimum_price import calculate_minimum_price
from price_tracker.const import (
    COLUMN_COMPETITOR_DELIVERY_LOCATIONS,
    COLUMN_COMPETITOR_OFFER_PRICE,
    COLUMN_COMPETITOR_FINAL_PRICE,
    COLUMN_COMPETITOR_MIN_QUANTITY,
    COLUMN_COMPETITOR_QUANTITY_BASED_DISCOUNT,
    COLUMN_PRODUCT_DELIVERY_LOCATIONS,
    COLUMN_PRODUCT_QAUNTITY,
)


def filter_competitors_details(
    product: pd.Series, competitors_details: pd.DataFrame
) -> pd.DataFrame:
    log = logging.getLogger("price_tracker.filter_competitors_details")
    log.debug("Filtering competitor details")
    # Select relevant columns
    relevant_columns = [
        COLUMN_COMPETITOR_OFFER_PRICE,
        COLUMN_COMPETITOR_DELIVERY_LOCATIONS,
        COLUMN_COMPETITOR_QUANTITY_BASED_DISCOUNT,
        COLUMN_COMPETITOR_MIN_QUANTITY,
    ]
    competitors_details = competitors_details[relevant_columns]
    competitors_details.loc[:, COLUMN_COMPETITOR_MIN_QUANTITY] = (
        competitors_details.loc[:, COLUMN_COMPETITOR_MIN_QUANTITY].astype(int)
    )

    mask = (product[COLUMN_PRODUCT_QAUNTITY] <= 0) | (
        product[COLUMN_PRODUCT_QAUNTITY]
        >= competitors_details[COLUMN_COMPETITOR_MIN_QUANTITY]
    )

    competitors_details = competitors_details[mask]

    # Filter by delivery locations
    if len(product[COLUMN_PRODUCT_DELIVERY_LOCATIONS]) != 0:
        delivery_locations_regex = "|".join(COLUMN_PRODUCT_DELIVERY_LOCATIONS)
        competitors_details = competitors_details[
            competitors_details[COLUMN_COMPETITOR_DELIVERY_LOCATIONS].str.contains(
                delivery_locations_regex
            )
        ]

    # Convert Offer Price to float
    competitors_details.loc[:, COLUMN_COMPETITOR_OFFER_PRICE] = (
        competitors_details.loc[:, COLUMN_COMPETITOR_OFFER_PRICE]
        .str.replace("₹", "")
        .str.replace(",", "")
        .astype(float)
    )

    # Adjust Offer Price based on Quantity based Discount
    competitors_details[COLUMN_COMPETITOR_FINAL_PRICE] = competitors_details.apply(
        lambda row: calculate_minimum_price(row, product), axis=1
    )

    if product[COLUMN_PRODUCT_QAUNTITY] > 0:
        competitors_details = competitors_details[
            product[COLUMN_PRODUCT_QAUNTITY]
            * competitors_details[COLUMN_COMPETITOR_FINAL_PRICE]
            <= 25000
        ]
    else:
        competitors_details = competitors_details[
            competitors_details[COLUMN_COMPETITOR_MIN_QUANTITY].astype(int)
            * competitors_details[COLUMN_COMPETITOR_FINAL_PRICE]
            <= 25000
        ]
    return competitors_details
