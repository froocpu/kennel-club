import json
import logging
import os

from bs4 import BeautifulSoup

from full_pedigree.config import *
from full_pedigree.data import prepare_d3_stratify_data, write_d3_stratify_data
from full_pedigree.dogs import DoggoUnit
from full_pedigree.scrape import BASE_URL, get_html_doc
from full_pedigree.utils import parse_arguments_get_full_pedigree, get_url

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


def get_full_pedigree():
    url = get_url(args)
    for dog in get_dogs(url):
        doggy_dict.update({
            dog.name: dog.dict()
        })
    with open(DOG_DICT_LOCATION, "w") as dd:
        output_text = json.dumps(doggy_dict)
        dd.write(output_text)
    return doggy_dict


if __name__ == "__main__":
    doggy_dict = {}

    args = parse_arguments_get_full_pedigree()
    if args.noscrape:
        with open(DOG_DICT_LOCATION, 'r') as dd:
            data = json.loads(''.join(dd.readlines()))
            logger.info(f"Number of rows read from pre-generated data file: {len(data)}")
    else:
        get_full_pedigree()

    d3_data = prepare_d3_stratify_data(data)
    write_d3_stratify_data(d3_data)
    logger.info(f"Number of rows written to new data file: {len(d3_data)}")

