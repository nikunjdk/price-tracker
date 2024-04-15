import logging
import pandas as pd

from price_tracker.const import (
    COLUMN_PRODUCT_CURRENT_PRICE,
    COLUMN_PRODUCT_DELIVERY_LOCATIONS,
    COLUMN_PRODUCT_QAUNTITY,
    COLUMN_PRODUCT_URL,
)
from price_tracker.delivery_location import process_delivery_locations


def get_products_from_excel(
    excel_file: str, quantity: int, delivery_locations: list[str]
) -> pd.DataFrame:
    """
    Reads an Excel file containing product data and extracts 'URL' and 'CURRENT PRICE' columns.

    Args:
        excel_file (str): The name of the Excel file to read.

    Returns:
        pd.DataFrame: A DataFrame containing the 'URL' and 'CURRENT PRICE' columns.

    Raises:
        FileNotFoundError: If the specified file is not found.
        KeyError: If the columns 'URL' and/or 'CURRENT PRICE' are not found.
        Exception: If no products are found in the file.

    Example:
        >>> products_df = get_products_from_excel("products.xlsx")
        >>> print(products_df.head())
                   URL  CURRENT PRICE
        0  example.com/product1          49.99
        1  example.com/product2          29.99
        ...
    """
    log = logging.getLogger("price_tracker.get_products_from_excel")
    try:
        products = pd.read_excel(excel_file)
        if COLUMN_PRODUCT_URL not in products.columns:
            raise KeyError("'URL' column not found")
        if COLUMN_PRODUCT_CURRENT_PRICE not in products.columns:
            raise KeyError("CURRENT PRICE column not found")
        if COLUMN_PRODUCT_QAUNTITY not in products.columns:
            products[COLUMN_PRODUCT_QAUNTITY] = quantity
        else:
            products[COLUMN_PRODUCT_QAUNTITY] = products[COLUMN_PRODUCT_QAUNTITY].apply(
                lambda x: int(x) if pd.notna(x) else x
            )
            products[COLUMN_PRODUCT_QAUNTITY] = products[
                COLUMN_PRODUCT_QAUNTITY
            ].fillna(quantity)
        if COLUMN_PRODUCT_DELIVERY_LOCATIONS not in products.columns:
            products[COLUMN_PRODUCT_DELIVERY_LOCATIONS] = delivery_locations
        else:
            products[COLUMN_PRODUCT_DELIVERY_LOCATIONS] = products[
                COLUMN_PRODUCT_DELIVERY_LOCATIONS
            ].apply(lambda value: process_delivery_locations(value, delivery_locations))
    except FileNotFoundError:
        raise FileNotFoundError(f"{excel_file} file not found")
    except Exception as e:
        log.error(e)
        raise
    else:
        if products.empty:
            raise Exception(f"No products found in {excel_file}")
        return products


def get_products_from_params(
    url: str,
    current_price: float | None,
    quantity: int | None,
    delivery_locations: list[str],
) -> pd.DataFrame:
    data = {
        COLUMN_PRODUCT_URL: [url],
        COLUMN_PRODUCT_CURRENT_PRICE: [current_price],
        COLUMN_PRODUCT_QAUNTITY: [quantity],
        COLUMN_PRODUCT_DELIVERY_LOCATIONS: [delivery_locations],
    }
    return pd.DataFrame(data)
