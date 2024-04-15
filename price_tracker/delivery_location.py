import pandas as pd


def is_delivery_location(delivery_location: str) -> bool:
    delivery_locations = (
        "ANDHRA PRADESH",
        "ARUNACHAL PRADESH ",
        "ASSAM",
        "BIHAR",
        "CHHATTISGARH",
        "GOA",
        "GUJARAT",
        "HARYANA",
        "HIMACHAL PRADESH",
        "JAMMU AND KASHMIR",
        "JHARKHAND",
        "KARNATAKA",
        "KERALA",
        "MADHYA PRADESH",
        "MAHARASHTRA",
        "MANIPUR",
        "MEGHALAYA",
        "MIZORAM",
        "NAGALAND",
        "ODISHA",
        "PUNJAB",
        "RAJASTHAN",
        "SIKKIM",
        "TAMIL NADU",
        "TELANGANA",
        "TRIPURA",
        "UTTAR PRADESH",
        "UTTARAKHAND",
        "WEST BENGAL",
        "ANDAMAN AND NICOBAR ISLANDS",
        "CHANDIGARH",
        "DADRA AND NAGAR HAVELI",
        "DAMAN AND DIU",
        "LAKSHADWEEP",
        "NATIONAL CAPITAL TERRITORY OF DELHI",
        "PUDUCHERRY",
        "All India",
    )
    return delivery_location in delivery_locations


def process_delivery_locations(
    delivery_location: pd.Series, default_locations: list[str]
) -> list[str]:
    if not delivery_location:
        return default_locations
    locations = delivery_location.split(", ")
    for loc in locations:
        if not is_delivery_location(loc):
            raise ValueError(f"Invalid delivery location: {loc}")
    return locations
