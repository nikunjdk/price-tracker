import pandas as pd


def get_products_from_excel(excel_file: str) -> pd.DataFrame:
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
    try:
        products = pd.read_excel(excel_file, usecols=["URL", "CURRENT PRICE"])
    except FileNotFoundError:
        raise FileNotFoundError(f"{excel_file} file not found")
    except ValueError as e:
        if "URL" in str(e) and "CURRENT PRICE" in str(e):
            raise ValueError("'URL' and 'CURRENT PRICE' columns not found")
        elif "CURRENT PRICE" in str(e):
            raise ValueError("'CURRENT PRICE' column not found")
        elif "URL" in str(e):
            raise ValueError("'URL' column not found")
        raise
    except Exception:
        raise
    else:
        if products.empty:
            raise Exception(f"No products found in {excel_file}")
        return products
