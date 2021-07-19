from requests import get
from bs4 import BeautifulSoup
import pprint


def get_country_code(lang):
    url = f'https://wiki2.org/{lang}/ISO_3166-2'
    params = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0"
    }
    r = get(url, params=params)
    soup = BeautifulSoup(r.text, 'lxml').find(
        name='table', class_='wikitable sortable')
    lines = soup.find_all(name='tr')[1:len(soup.find_all(name='tr'))+1]
    codes_with_countries = []
    for line in lines:
        code_country = {}
        code = BeautifulSoup(
            str(BeautifulSoup(str(line), 'lxml').findAll('a')[0]), 'lxml').text
        country = BeautifulSoup(
            str(BeautifulSoup(str(line), 'lxml').findAll('a')[1]), 'lxml').text
        code_country[code] = str(country).replace('\u2005', ' ')
        codes_with_countries.append(code_country)
    return codes_with_countries


if __name__ == "__main__":
    pprint.pprint(get_country_code())
