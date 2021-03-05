from scrape import SELECTOR


class Doggo:
    def __init__(self, name, sex=None, colour=None, dob=None, link=None, sire=None, dam=None):
        self.name = name
        self.sex = sex
        self.colour = colour
        self.dob = dob
        self.link = link
        self.sire = sire
        self.dam = dam

    def __str__(self):
        return f'{"name":"{self.name}", "link":"{self.link}", "sire":"{self.sire}", "dam":"{self.dam}"}'

    def dict(self):
        return {"name": self.name,
                "link": self.link,
                "sire": self.sire,
                "dam": self.dam,
                "colour": self.colour,
                "sex": self.sex,
                "dob": self.dob}


class DoggoUnit:
    """
    Assuming the order is always the same:
    0. Original dog
    1. Dad
    2. Dad's dad
    3. Dad's mum
    4. Mum
    5. Mum's dad
    6. Mum's mum
    """
    def __init__(self, soup):
        profile = get_dog_profile(soup)
        results = soup.findAll("div", {"class": SELECTOR})
        links = []
        names = []
        for result in results:
            names.append(result.text.strip())
            link = result.find('a', href=True)
            links.append(link['href'] if link else None)

        self.top_dog = Doggo(
            name=names[0],
            link=links[0],
            sire=links[1],
            dam=links[4],
            colour=profile.get('colour'),
            sex=profile.get('sex'),
            dob=profile.get('dob')
        )

        self.sire = Doggo(
            name=names[1],
            link=links[1]
        )
        self.dam = Doggo(
            name=names[4],
            link=links[4]
        )


def get_dog_profile(soup):

    dog_header_details = soup.findAll('dd', {'class': 'o-dog-header__details-value'})

    # Sex
    if 'a-icon--male' in _get_sex_svg_icon(dog_header_details):
        sex = 'Male'
    elif 'a-icon--female' in _get_sex_svg_icon(dog_header_details):
        sex = 'Female'
    else:
        sex = '?'

    # Sometimes colour is missing, but sex and DOB are always present.
    if len(dog_header_details) == 3:
        colour = dog_header_details[1].text
        birthday = dog_header_details[2].text
    else:
        colour = '?'
        birthday = dog_header_details[1].text

    return {'sex': sex, 'colour': colour, 'dob': birthday}


def _get_sex_svg_icon(tag):
    return tag[0].contents[0].attrs.get('class')