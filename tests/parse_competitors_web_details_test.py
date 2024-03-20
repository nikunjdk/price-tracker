import pytest
from bs4 import BeautifulSoup, Tag
from price_tracker.parse_competitors_web_details import parse_competitors_web_details


@pytest.fixture
def sample_competitors_url_soup():
    # Create a sample BeautifulSoup object with relevant structure
    html = """
    <div id="sellers-table-wrap">
        <table>
            <tr><td>Product A</td><td>100</td></tr>
            <tr><td>Product B</td><td>80</td></tr>
        </table>
    </div>
    """
    return BeautifulSoup(html, "html.parser")


def test_valid_competitors_table(sample_competitors_url_soup):
    # Call the function with a valid table
    parsed_details = parse_competitors_web_details(
        "https://example.com", sample_competitors_url_soup
    )

    # Assert that the parsed details match the expected data
    assert len(parsed_details) == 2
    assert parsed_details[0] == ["Product A", "100"]
    assert parsed_details[1] == ["Product B", "80"]


def test_missing_div(sample_competitors_url_soup):
    # Modify the soup to simulate missing 'sellers-table-wrap' div
    sample_competitors_url_soup.find(
        "div", attrs={"id": "sellers-table-wrap"}
    ).decompose()

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Competitor price table not found"):
        parse_competitors_web_details(
            "https://example.com", sample_competitors_url_soup
        )


def test_invalid_table(sample_competitors_url_soup):
    # Modify the soup to simulate missing 'table' within 'sellers-table-wrap'
    sample_competitors_url_soup.find("table").decompose()

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Competitor price table not found"):
        parse_competitors_web_details(
            "https://example.com", sample_competitors_url_soup
        )


def test_non_tag_table(sample_competitors_url_soup):
    # Modify the soup to simulate 'competitors_prices_table' not being a Tag
    sample_competitors_url_soup.find("table").replace_with("Not a Tag")

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Competitor price table not found"):
        parse_competitors_web_details(
            "https://example.com", sample_competitors_url_soup
        )


def test_empty_table(sample_competitors_url_soup):
    # Modify the soup to simulate an empty table
    sample_competitors_url_soup.find("table").decompose()

    # Call the function and expect an exception
    with pytest.raises(Exception, match="Competitor price table not found"):
        parse_competitors_web_details(
            "https://example.com", sample_competitors_url_soup
        )


if __name__ == "__main__":
    pytest.main()
