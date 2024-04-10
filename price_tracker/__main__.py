import os
from datetime import datetime
from tqdm import tqdm
from get_products import get_products_from_excel
from init_argparse import init_argparse
from setup_logging import setup_logging
from process_product import process_product
from multiprocessing import Pool, cpu_count
from functools import partial


def main():
    try:
        current_date_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file_name = "logs/price_tracker_%s.log" % current_date_time
        log = setup_logging(log_file_name)

        excel_file_name = "Gem comparison products copy.xlsx"
        products = get_products_from_excel(excel_file_name)

        # Create a multiprocessing Pool
        pool = Pool(cpu_count())

        # Use the pool to process the products in parallel
        min_competitor_prices = list(
            tqdm(
                pool.imap(
                    process_product, [product for _, product in products.iterrows()]
                ),
                total=len(products),
                desc="Number of products processed",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [time spent: {elapsed}, time left: {remaining}]",
            )
        )

        pool.close()
        pool.join()

        log.debug("Finished processing all products")
        products["MINIMUM PRICE"] = min_competitor_prices
        if not os.path.exists("results"):
            os.mkdir("results")
        products.to_excel(
            f"results/price_tracker_{current_date_time}.xlsx",
            index=False,
            header=["URL", "CURRENT PRICE", "MINIMUM PRICE"],
        )

    except Exception as e:
        log.error(e, exc_info=True)


if __name__ == "__main__":
    # Initialize parser
    parser = init_argparse()
    args = parser.parse_args()
    main()
