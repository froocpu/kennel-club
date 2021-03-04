import requests


def get_html_doc(url):
    response = requests.get(url)
    return response.text


BASE_URL = "https://www.thekennelclub.org.uk"
SELECTOR = "m-pedigree-graph__dog-name"