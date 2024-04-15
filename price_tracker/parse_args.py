import argparse
import importlib.metadata


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Price tracker for GEM Portal",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} {importlib.metadata.version(parser.prog)}",
    )
    parser.add_argument(
        "--excel_file_path",
        type=str,
        help="Path to the Excel file. It is required if product url and current price is not given",
    )
    parser.add_argument(
        "--product_url",
        type=str,
        help="URL of the product. It is required if excel file path is not given",
    )
    parser.add_argument(
        "--current_price",
        type=float,
        help="Current price of the product. It is required if excel file path is not given",
    )
    parser.add_argument(
        "--delivery_locations",
        nargs="*",
        type=str,
        default=[],
        help='Delivery locations of the product. It should be from the following list: "ANDHRA PRADESH","ARUNACHAL PRADESH ","ASSAM","BIHAR","CHHATTISGARH","GOA","GUJARAT","HARYANA","HIMACHAL PRADESH","JAMMU AND KASHMIR","JHARKHAND","KARNATAKA","KERALA","MADHYA PRADESH","MAHARASHTRA","MANIPUR","MEGHALAYA","MIZORAM","NAGALAND","ODISHA","PUNJAB","RAJASTHAN","SIKKIM","TAMIL NADU","TELANGANA","TRIPURA","UTTAR PRADESH","UTTARAKHAND","WEST BENGAL","ANDAMAN AND NICOBAR ISLANDS","CHANDIGARH","DADRA AND NAGAR HAVELI","DAMAN AND DIU","LAKSHADWEEP","NATIONAL CAPITAL TERRITORY OF DELHI","PUDUCHERRY","All India". EG: --delivery_locations "TAMIL NADU" "All India".',
    )
    parser.add_argument(
        "--quantity", type=int, default=-1, help="Quantity of the product."
    )
    args = parser.parse_args()

    # Check the conditions
    if not args.excel_file_path and (not args.product_url or not args.current_price):
        parser.error(
            "Either excel_file_path or both product_url and current_price are required."
        )

    return args
