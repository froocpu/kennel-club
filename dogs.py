from scrape import SELECTOR


class Doggo:
    def __init__(self, name, link=None, sire=None, dam=None):
        self.name = name
        self.link = link
        self.sire = sire
        self.dam = dam

    def __str__(self):
        return f'{"name":"{self.name}", "link":"{self.link}", "sire":"{self.sire}", "dam":"{self.dam}"}'

    def dict(self):
        return {"name": self.name, "link": self.link, "sire": self.sire, "dam": self.dam}


class DoggoFamily:

    def __init__(self, soup):
        results = soup.findAll("div", {"class": SELECTOR})
        links = []
        names = []
        for result in results:
            names.append(result.text.strip())
            link = result.find('a', href=True)
            links.append(link['href'] if link else None)

        """
        Assuming the order is the same:

        0. Original dog
        1. Dad
        2. Dad's dad
        3. Dad's mum
        4. Mum
        5. Mum's dad
        6. Mum's mum
        """

        # Build_tree
        self.top_dog = Doggo(
            name=names[0],
            link=links[0],
            sire=links[1],
            dam=links[2]
        )
        self.sire = Doggo(
            name=names[1],
            link=links[1]
        )
        self.dam = Doggo(
            name=names[4],
            link=links[4]
        )