from price_tracker.const import (
    COLUMN_COMPETITOR_OFFER_PRICE,
    COLUMN_COMPETITOR_QUANTITY_BASED_DISCOUNT,
    COLUMN_PRODUCT_QAUNTITY,
)
import pandas as pd
import re


def calculate_minimum_price(row: pd.Series, product: pd.Series) -> float:
    if (
        pd.isnull(row[COLUMN_COMPETITOR_QUANTITY_BASED_DISCOUNT])
        or row[COLUMN_COMPETITOR_QUANTITY_BASED_DISCOUNT] == ""
    ):
        return row[COLUMN_COMPETITOR_OFFER_PRICE]
    else:
        discounts = row[COLUMN_COMPETITOR_QUANTITY_BASED_DISCOUNT].split("\n")
        minimum_price = row[COLUMN_COMPETITOR_OFFER_PRICE]
        for discount in discounts:
            units, discount_amount = discount.split(" = ")
            discount_amount = float(discount_amount.replace("₹", "").replace(",", ""))
            start, end = map(int, re.findall(r"\d+", units))
            if product[COLUMN_PRODUCT_QAUNTITY] > 0:
                if start <= product[COLUMN_PRODUCT_QAUNTITY] <= end:
                    return row[COLUMN_COMPETITOR_OFFER_PRICE] - discount_amount
            else:
                minimum_price = (
                    row[COLUMN_COMPETITOR_OFFER_PRICE] - discount_amount
                    if row[COLUMN_COMPETITOR_OFFER_PRICE] - discount_amount
                    < minimum_price
                    else minimum_price
                )
        return minimum_price
