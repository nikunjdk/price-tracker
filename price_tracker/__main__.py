import logging
import os
from datetime import datetime
from tqdm import tqdm 
from get_products import get_products_from_excel
from process_product import process_product

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

        for _, product in tqdm(products.iterrows(), desc="Number of products processed", total=len(products), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [time spent: {elapsed}, time left: {remaining}]"):
            min_competitor_prices.append(process_product(product))

        log.debug("Finished processing all products")
        products["MINIMUM PRICE"] = min_competitor_prices
        if not os.path.exists("results"):
            os.mkdir("results")
        products.to_excel(f"results/price_tracker_{current_date_time.strftime('%Y%m%d-%H%M%S')}.xlsx",
                          index=False, header=["URL", "CURRENT PRICE", "MINIMUM PRICE"])

    except Exception as e:
        log.error(f"Error in main function: {e}", exc_info=True)

    #     min_competitor_prices = []
    #     number_of_products = len(products)

    #     for count, product in products.iterrows():
    #         try:
    #             log.debug(f"Processing product: {int(str(count)) + 1} of {number_of_products}")
    #             product_url = product["URL"]
    #             competitors_details = get_competitors_details(product_url)
    #             filtered_competitors_details = filter_competitors_details(
    #                 competitors_details, delivery_locations=["TAMIL NADU", "All India"]
    #             )
    #             min_competitor_prices.append(
    #                 filtered_competitors_details["Offer Price"].min()
    #             )
    #         except Exception as e:
    #             log.error(f"Error in processing {int(str(count)) + 1}th product ({product["URL"]}): {e}", stack_info=True)
            
    #     log.debug("Finished processing all products")
    #     products["MINIMUM PRICE"] = min_competitor_prices
    #     if not os.path.exists("results"):
    #         os.mkdir("results")
    #     products.to_excel(f"results/price_tracker_{current_date_time.strftime("%Y%m%d-%H%M%S")}.xlsx", index=False, header=["URL", "CURRENT PRICE", "MINIMUM PRICE"])
    # except Exception as e:
    #     log.error(e, exc_info=True)


if __name__ == "__main__":
    main()
