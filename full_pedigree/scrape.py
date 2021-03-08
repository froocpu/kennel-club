import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_html_doc(url):
    s = requests.Session()
    retries = Retry(total=5, backoff_factor=1)
    s.mount('https://', HTTPAdapter(max_retries=retries))
    response = s.get(url)
    return response.text


BASE_URL = "https://www.thekennelclub.org.uk"
SELECTOR = "m-pedigree-graph__dog-name"