import pytest
import pandas as pd
from price_tracker.get_products import get_products_from_excel


@pytest.fixture
def sample_excel_file(tmp_path):
    # Create a sample Excel file with relevant columns
    excel_file = tmp_path / "products.xlsx"
    data = {
        COLUMN_PRODUCT_URL: ["example.com/product1", "example.com/product2"],
        COLUMN_PRODUCT_CURRENT_PRICE: [49.99, 29.99],
    }
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False)
    return excel_file


def test_valid_file(sample_excel_file):
    # Call the function
    products_df = get_products_from_excel(sample_excel_file)

    # Assert that the returned DataFrame has the expected columns
    assert COLUMN_PRODUCT_URL in products_df.columns
    assert COLUMN_PRODUCT_CURRENT_PRICE in products_df.columns


def test_missing_file():
    # Test behavior when the file does not exist
    with pytest.raises(Exception, match="nonexistent_file.xlsx file not found"):
        get_products_from_excel("nonexistent_file.xlsx")


@pytest.mark.parametrize(
    "excel_data, exception",
    [
        (
            {
                COLUMN_PRODUCT_URL: ["example.com/product1", "example.com/product2"],
            },
            "'CURRENT PRICE' column not found",
        ),
        (
            {
                COLUMN_PRODUCT_CURRENT_PRICE: [49.99, 29.99],
            },
            "'URL' column not found",
        ),
        (
            {
                "INVALID": [1, 2],
            },
            "'URL' and 'CURRENT PRICE' columns not found",
        ),
    ],
)
def test_missing_columns(tmp_path, excel_data, exception):
    # Create an Excel file with missing columns
    excel_file = tmp_path / "missing_columns.xlsx"
    data = excel_data
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False)

    # Call the function
    with pytest.raises(ValueError, match=exception):
        get_products_from_excel(excel_file)


def test_missing_products(tmp_path):
    # Create an Excel file with no products
    excel_file = tmp_path / "missing_products.xlsx"
    data = {COLUMN_PRODUCT_URL: [], COLUMN_PRODUCT_CURRENT_PRICE: []}
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False)

    # Call the function
    with pytest.raises(Exception, match=f"No products found"):
        get_products_from_excel(excel_file)
