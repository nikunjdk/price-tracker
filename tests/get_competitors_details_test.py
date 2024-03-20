# test_my_module.py

import pytest
from bs4 import BeautifulSoup
from price_tracker.get_competitors_details import get_competitors_details


@pytest.fixture
def sample_competitors_url_soup():
    # Create a sample BeautifulSoup object with relevant structure for testing
    html = """
    <div id="sellers-table-wrap">
        <table>
            <tr><td>Seller A</td><td>100</td></tr>
            <tr><td>Seller B</td><td>80</td></tr>
        </table>
    </div>
    """
    return BeautifulSoup(html, "html.parser")


@pytest.fixture
def sample_competitors_url_data():
    # Create a sample BeautifulSoup object with relevant structure for testing
    html = """
    <div id="sellers-table-wrap">
        <table>
            <tr><td>Seller A</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr>
            <tr><td>Seller B</td><td>80</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td><td>100</td></tr>
        </table>
    </div>
    """
    return html


def test_valid_competitors_details(sample_competitors_url_data, mocker):
    # Mock requests.get to avoid actual network call
    mocker.patch(
        "requests.get", return_value=mocker.Mock(content=sample_competitors_url_data)
    )

    # Call the function with a valid competitors URL
    parsed_details = get_competitors_details("https://example.com/product123.html")

    # Assert that the parsed details match the expected data
    assert len(parsed_details) == 2
    assert len(parsed_details.iloc[0]) == 8
    assert parsed_details.iloc[0]["Sellers"] == "Seller A"
    assert parsed_details.iloc[1]["Offer Price"] == "80"


def test_missing_competitors_table(sample_competitors_url_soup, mocker):
    # Modify the soup to simulate missing 'sellers-table-wrap' div
    sample_competitors_url_soup.find(
        "div", attrs={"id": "sellers-table-wrap"}
    ).decompose()

    # Mock requests.get to avoid actual network call
    mocker.patch("requests.get", return_value=mocker.Mock(content=b""))

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Competitor price table not found"):
        get_competitors_details("https://example.com/product456.html")


# Add more test cases for other scenarios (e.g., invalid table, empty table, etc.)

if __name__ == "__main__":
    pytest.main()
