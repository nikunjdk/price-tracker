import argparse
import importlib.metadata


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Price tracker for GEM Portal",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} {importlib.metadata.version(parser.prog)}",
    )
    file_arg_group = parser.add_argument_group("file")
    file_arg_group.add_argument("-f", "--excel_file_path")

    individual_arg_group = parser.add_argument_group("individual")
    individual_arg_group.add_argument("-url", "--product_link")
    individual_arg_group.add_argument("-l", "--locations")
    return parser
