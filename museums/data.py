from bs4 import BeautifulSoup

from museums.tasks import extract_data
from museums.model import Museum, Country

import re
import time
import wikipedia
import pycountry


regex = r"(\d{4}).*"
countries = pycountry.countries


def extract_list_of_museum_data():
    def find_country_by_name(name):
        def filter_func(x):
            return (hasattr(x, 'common_name') and x.common_name.lower() == name) or \
                x.name.lower().startswith(name)

        name = name.lower()
        if name.startswith('vatican'):
            name = 'Holy See (Vatican City State)'.lower()
        elif name.startswith('south korea'):
            name = 'Korea, Republic of'.lower()

        temp = list(filter(lambda x: x.name.lower() == name, countries))
        if len(temp) == 0:
            temp = list(filter(filter_func, countries))
            if len(temp) == 0:
                raise ValueError("invalid country " + name)
        x = temp[0]

        return Country(x.alpha_2, x.name)

    m = wikipedia.page('List_of_most_visited_museums')
    soup = BeautifulSoup(m.html(), 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')[2:]
    
    for row in rows:
        cells = row.find_all('td')
        name = cells[0].find('a').attrs['title']

        cell_links = cells[1].find_all('a')
        country_name = cell_links[0].attrs['title']

        country = find_country_by_name(country_name)
        city = cell_links[1].attrs['title']
        visits = int(cells[2].text.replace(',', ''))

        matches = list(re.finditer(regex, str(cells[3].text), re.MULTILINE))
        year = int(matches[0].groups()[0])

        extract_data(Museum(name, country, city, visits, -1, year))
