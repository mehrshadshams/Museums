import time
import pandas as pd
import requests

from museums.model import Museum
from pymongo import MongoClient
from . import celery

# change the ip and port to your mongo database's
client = MongoClient('database', 27017)
db = client.mongodb_test
collection = db.museums

un_city_pop = pd.read_csv(
    "https://raw.githubusercontent.com/mehrshadshams/Museums/master/data.csv")
un_city_pop = un_city_pop[un_city_pop['Sex'] == 'Both Sexes']
un_city_pop.City = un_city_pop.City.str.lower()


# To Deal with name differences between Wikipedia and UN data export
def normalize_country_name(name):
    if '(' in name:
        idx = name.index('(')
        if idx >= 0:
            name = name[:idx].strip()
    return name


def normalize_city_name(name):
    if "," in name:
        idx = name.index(',')
        if idx >= 0:
            name = name[:idx].strip()
    return name


@celery.task(bind=True, default_retry_delay=10)
def extract_data(self, museum):
    population = get_city_population(museum.city, museum.country)
    collection.insert(Museum(museum.name, museum.country,
                             museum.city, museum.visitors, population, museum.year)._asdict())


@celery.task(bind=True, default_retry_delay=10)
def get_city_population(self, city, country):
    country_name = normalize_country_name(country.name)
    city_name = normalize_city_name(city.lower())

    print("Find population for Country='{0}', City='{1}'".format(country.name, city))
    url = "https://public.opendatasoft.com/api/records/1.0/search/?dataset=worldcitiespop&q={0}&sort=population&facet=country&refine.country={1}"
    req = requests.get(url.format(city_name, country.alpha_2.lower()))
    req.raise_for_status()

    data = req.json()

    if len(data) > 0:
        records = data['records']
        if len(records) > 0:
            fields = records[0]['fields']
            if 'population' in fields:
                return fields['population']

    if city_name.endswith('city'):
        city_name = city_name[:city_name.index('city')].strip()
        return get_city_population(city_name, country)
    else:
        df = un_city_pop[un_city_pop['Country or Area'].str.contains(country_name, na=False)]
        df = df[df['City'].str.contains(city_name, na=False)].sort_values(['Year'], ascending=False)
        if len(df) > 0:
            return int(df[0:1]['Value'].values[0])

    return -1


# set a retry delay, 10 equal to 10s
@celery.task(bind=True, default_retry_delay=10)
def longtime_add(self, i):
    print('long time task begins: ' + str(i))
    try:
        r = requests.get(i)
        # store status code and current time to mongodb
        # post.insert({'status': r.status_code, "create_time": time.time()})
        print('long time task finished')
    except Exception as exc:
        raise self.retry(exc=exc)
    return r.status_code
