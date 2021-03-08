import argparse

from full_pedigree.config import DEFAULT_STARTING_DOG
from full_pedigree.scrape import BASE_URL


def parse_arguments_get_full_pedigree():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="starting dogId", default=DEFAULT_STARTING_DOG, required=False)
    parser.add_argument("--noscrape",
                        help="When flagged, it will not scrape data from kennel club, and instead work with local data.",
                        action="store_true")
    args = parser.parse_args()
    return args


def get_url(arguments):
    if arguments.start:
        url_search_part = f"/search/dog-profile/?dogId={arguments.start}"
    else:
        url_search_part = f"/search/dog-profile/?dogId={DEFAULT_STARTING_DOG}"

    return f"{BASE_URL}{url_search_part}"
