from datetime import datetime
import logging
import os
from get_products import get_products_from_excel
from filter_competitors_details import filter_competitors_details
from get_competitors_details import get_competitors_details

def setup_logging(log_file_name: str) -> logging.Logger:
    logging.getLogger("price_tracker")
    if not os.path.exists("tmp"):
        os.mkdir("tmp")

        
    logger = logging.getLogger('price_tracker')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(log_file_name, "w")
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger

def main():
    current_date_time = datetime.now()
    log_file_name = f"tmp/price_tracker_{current_date_time.strftime("%Y%m%d-%H%M%S")}.log"
    log = setup_logging(log_file_name)

    try:
        excel_file_name = "Gem comparison products copy.xlsx"
        products = get_products_from_excel(excel_file_name)
        min_competitor_prices = []

        for _, product in products.iterrows():
            log.debug(f"Processing product: {_}")
            product_url = product["URL"]
            # product_current_price = product["CURRENT PRICE"]
            competitors_details = get_competitors_details(product_url)
            filtered_competitors_details = filter_competitors_details(
                competitors_details, delivery_locations=["TAMIL NADU", "All India"]
            )
            min_competitor_prices.append(
                filtered_competitors_details["Offer Price"].min()
            )
        log.debug("Finished processing all products")
        products["MINIMUM PRICE"] = min_competitor_prices
        if not os.path.exists("results"):
            os.mkdir("results")
        products.to_excel(f"results/price_tracker_{current_date_time.strftime("%Y%m%d-%H%M%S")}.xlsx", index=False, header=["URL", "CURRENT PRICE", "MINIMUM PRICE"])
    except Exception as e:
        log.error(e, stack_info=True)


if __name__ == "__main__":
    main()
