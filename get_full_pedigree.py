import argparse
import json
import logging
import os

from bs4 import BeautifulSoup

from config import DEFAULT_STARTING_DOG
from data import prepare_d3_stratify_data, write_d3_stratify_data
from dogs import DoggoUnit
from scrape import BASE_URL, get_html_doc

logging.basicConfig(
    level=os.environ.get("LOGGING_LEVEL", "INFO"),
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def get_dogs(link: str, generation: int = 0):
    logger.info(link)
    html_doc = get_html_doc(link)
    soup = BeautifulSoup(html_doc)
    doggy_tree = DoggoUnit(soup, generation)

    logger.info(f"Dog scraped: '{doggy_tree.top_dog.name}'")
    if doggy_tree.top_dog.name in doggy_dict.keys():
        return
    yield doggy_tree.top_dog

    logger.info(f"Generation: {generation}")
    if doggy_tree.dam.link:
        logger.debug(f"Checking {doggy_tree.top_dog.name}'s dam's line....")
        yield from get_dogs(f"{BASE_URL}{doggy_tree.dam.link}", generation=generation+1)
    if doggy_tree.sire.link:
        logger.debug(f"Checking {doggy_tree.top_dog.name}'s sire's line....")
        yield from get_dogs(f"{BASE_URL}{doggy_tree.sire.link}", generation=generation+1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="starting dogId", default=DEFAULT_STARTING_DOG, required=False)
    parser.add_argument("--noscrape",
                        help="When flagged, it will not scrape data from kennel club, and instead work with local data.",
                        action="store_true")
    args = parser.parse_args()

    if args.noscrape:
        with open('doggy_dict.json', 'r') as dd:
            data = json.loads(''.join(dd.readlines()))
            logger.info(f"Number of rows read from pre-generated data file: {len(data)}")
    else:
        doggy_dict = {}

        if args.start:
            start_id = f"/search/dog-profile/?dogId={args.start}"
        else:
            start_id = DEFAULT_STARTING_DOG

        for dog in get_dogs(f"{BASE_URL}{start_id}"):
            doggy_dict.update({
                dog.name: dog
            })

        data = [dog.dict() for dog in doggy_dict.values()]
        with open('doggy_dict.json', 'w') as dd:
            dd.write(json.dumps(data))
            logger.info(f"Number of rows written to new data file: {len(data)}")

    d3_data = prepare_d3_stratify_data(data)
    write_d3_stratify_data(d3_data)

