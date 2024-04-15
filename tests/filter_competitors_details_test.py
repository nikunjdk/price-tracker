# test_my_module.py

import pandas as pd
import pytest
from price_tracker.filter_competitors_details import filter_competitors_details


@pytest.fixture
def sample_competitors_details():
    # Create a sample DataFrame with relevant data
    data = {
        "Offer Price": ["$100.00", "$800,000.12", "$120"],
        COLUMN_PRODUCT_DELIVERY_LOCATIONS: ["USA", "Canada", "Mexico"],
        "Quantity based Discount": ["", "8 to 99 units = $1,110", ""],
        "Min Quantity / Consignee": [10, 5000, 15],
    }
    return pd.DataFrame(data)


def test_valid_filter_competitors_details(sample_competitors_details):
    # Call the function with valid data
    filtered_details = filter_competitors_details(
        sample_competitors_details, ["USA", "Canada"]
    )

    # Assert that the filtered details match the expected data
    assert len(filtered_details) == 1
    assert filtered_details.iloc[0]["Offer Price"] == 100.0


def test_empty_filter_competitors_details(sample_competitors_details):
    # Modify the DataFrame to simulate empty results
    sample_competitors_details.drop(index=[0, 1], inplace=True)

    # Call the function and expect an empty DataFrame
    filtered_details = filter_competitors_details(
        sample_competitors_details, ["USA", "Canada"]
    )
    assert filtered_details.empty


# Add more test cases for other scenarios (e.g., invalid data, different delivery locations, etc.)

if __name__ == "__main__":
    pytest.main()
