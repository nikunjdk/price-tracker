from datetime import datetime
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from price_tracker.const import COLUMN_PRODUCT_MINIMUM_PRICE
from price_tracker.delivery_location import is_delivery_location
from price_tracker.get_products import get_products_from_excel, get_products_from_params
from price_tracker.parse_args import parse_args
from price_tracker.setup_logging import setup_logging
from price_tracker.get_min_competitor_price import get_min_competitor_price
from price_tracker.write_to_excel import write_to_excel


def main() -> None:
    try:
        current_date_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file_name = "logs/price_tracker_%s.log" % current_date_time
        log = setup_logging(log_file_name)

        args = parse_args()

        if len(args.delivery_locations) != 0:
            for delivery_loaction in args.delivery_locations:
                if is_delivery_location(delivery_loaction) == False:
                    raise ValueError("Invalid delivery location")

        products = (
            get_products_from_excel(
                args.excel_file_path, args.quantity, args.delivery_locations
            )
            if args.excel_file_path is not None
            else get_products_from_params(
                args.product_url,
                args.current_price,
                args.quantity,
                args.delivery_locations,
            )
        )

        # Create a multiprocessing Pool
        pool = Pool(cpu_count())

        # Use the pool to process the products in parallel
        min_competitor_prices = list(
            tqdm(
                pool.imap(
                    get_min_competitor_price,
                    [product for _, product in products.iterrows()],
                ),
                total=len(products),
                desc="Number of products processed",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [time spent: {elapsed}, time left: {remaining}]",
            )
        )

        pool.close()
        pool.join()

        log.debug("Finished processing all products")
        products[COLUMN_PRODUCT_MINIMUM_PRICE] = min_competitor_prices
        write_to_excel(current_date_time, products)

    except Exception as e:
        log.error(e, exc_info=True)


if __name__ == "__main__":
    main()
