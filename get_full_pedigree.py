import json

from bs4 import BeautifulSoup

from dogs import DoggoFamily
from scrape import BASE_URL, get_html_doc

ELTON = "/search/dog-profile/?dogId=10673831-d354-eb11-a812-000d3a874bc8"


def get_dogs(link):
    html_doc = get_html_doc(link)
    print(link)
    soup = BeautifulSoup(html_doc)
    doggy_tree = DoggoFamily(soup)
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

    doggy_dict = {}

    for dog in get_dogs(f"{BASE_URL}{ELTON}"):
        doggy_dict.update({
            dog.name: dog
        })

    print(doggy_dict)
    for i, j in doggy_dict.items():
        print(f"dog: {i}, sired by: {j.sire}, damed by: {j.dam}")

    output = [dog.dict() for dog in doggy_dict.values()]
    output_str = json.dumps(output)

    with open("dogs.json", "w") as dogs_file:
        dogs_file.write(output_str)

