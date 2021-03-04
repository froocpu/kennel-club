import argparse
import json

from bs4 import BeautifulSoup

from config import DEFAULT_STARTING_DOG
from data import prepare_nodes_and_links
from dogs import DoggoUnit
from scrape import BASE_URL, get_html_doc


def get_dogs(link: str):
    html_doc = get_html_doc(link)
    print(link)
    soup = BeautifulSoup(html_doc)
    doggy_tree = DoggoUnit(soup)
    print(f"Dis dogge: {doggy_tree.top_dog.name}")
    if doggy_tree.top_dog.name in doggy_dict.keys():
        return
    yield doggy_tree.top_dog
    if doggy_tree.dam.link:
        print(f"Checking {doggy_tree.top_dog.name}'s dam's line....")
        yield from get_dogs(f"{BASE_URL}{doggy_tree.dam.link}")
    if doggy_tree.sire.link:
        print(f"Checking {doggy_tree.top_dog.name}'s sire's line....")
        yield from get_dogs(f"{BASE_URL}{doggy_tree.sire.link}")


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
            print(len(data))
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

        print(len(doggy_dict))
        data = [dog.dict() for dog in doggy_dict.values()]
        with open('doggy_dict.json', 'w') as dd:
            dd.write(json.dumps(data))

    nodes_and_links = prepare_nodes_and_links(data)
    output_str = json.dumps(nodes_and_links)

    with open("d3/dogs.json", "w") as dogs_file:
        dogs_file.write(output_str)

