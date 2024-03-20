from typing import List
import pandas as pd


def filter_competitors_details(
    competitors_details: pd.DataFrame, delivery_locations: List[str]
) -> pd.DataFrame:
    # Select relevant columns
    relevant_columns = [
        "Offer Price",
        "Delivery Locations",
        "Quantity based Discount",
        "Min Quantity / Consignee",
    ]
    competitors_details = competitors_details[relevant_columns]

    # Filter by delivery locations
    delivery_locations_regex = "|".join(delivery_locations)
    competitors_details = competitors_details[
        competitors_details["Delivery Locations"].str.contains(delivery_locations_regex)
    ]

    # Convert Offer Price to float
    competitors_details["Offer Price"] = competitors_details["Offer Price"].str[1:]
    competitors_details["Offer Price"] = (
        competitors_details["Offer Price"].str.replace(",", "").astype(float)
    )

    # Adjust Offer Price based on Quantity based Discount
    competitors_details["Final Price"] = competitors_details.apply(
        determine_final_price, axis=1
    )

    # Drop rows where Min Quantity * Offer Price exceeds 25000
    competitors_details = competitors_details[
        competitors_details["Min Quantity / Consignee"].astype(int)
        * competitors_details["Final Price"]
        <= 25000
    ]

    return competitors_details


def determine_final_price(row):
    discount_info = row["Quantity based Discount"]

    if discount_info == "":
        return row["Offer Price"]

    discounts = discount_info.split("\n")
    final_price = row["Offer Price"]

    for discount_entry in discounts:
        discount_entry = discount_entry.strip()
        parts = discount_entry.split(" ")
        discount = float(parts[5][1:].replace(",", ""))
        price = row["Offer Price"] - discount
        min_quantity = int(parts[0])

        if price * min_quantity <= 25000 and price < final_price:
            final_price = price

    return final_price
