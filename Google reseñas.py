import requests
import json
import time
import pandas as pd

class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details


api = GooglePlaces("AIzaSyAoxhDWppkYjOKNjelGF9uBbQPRme2t9Tw")

places = api.search_places_by_coordinate("40.819057,-73.914048", "1000", "restaurant")

fields = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']


for place in places:
    details = api.get_place_details(place['place_id'], fields)

lista = {}

for place in places:
    details = api.get_place_details(place['place_id'], fields)
    try:
        website = details['result']['website']
    except KeyError:
        website = ""

    try:
        name = details['result']['name']
    except KeyError:
        name = ""

    try:
        address = details['result']['formatted_address']
    except KeyError:
        address = ""

    try:
        phone_number = details['result']['international_phone_number']
    except KeyError:
        phone_number = ""

    try:
        reviews = details['result']['reviews']
    except KeyError:
        reviews = []


    for review in reviews:

        rating = review['rating']
        text = review['text']



        lista[text] = "Rating:", rating, "Name of restaurant:", name, "Text:", text


lista

df = pd.DataFrame({'lista': lista})

df["lista"]

df.to_csv("df1.csv")
b = pd.read_csv("df1.csv")

#Cleaning and creation of "Rating"
b["Rating"] = b.lista.str.split(",", n=2).apply(lambda l: ":".join(l[:-1]))
b["Rating"] = b["Rating"].str.split("Rating:", n=1).apply(lambda l: ":".join(l[-1:]))
b["Rating"] = b["Rating"].str.split("':", n=1).apply(lambda l: ":".join(l[-1:]))
b["Rating"]

#Cleaning and creation of "Name_of_restaurant"
b["Name_of_restaurant"] = b.lista.str.split("Name of restaurant:", n=1).apply(lambda l: ":".join(l[1:]))
b["Name_of_restaurant"] = b.Name_of_restaurant.str.split("'Text:'", n=1).apply(lambda l: ":".join(l[:-1]))
b["Name_of_restaurant"] = b.Name_of_restaurant.str.split(",", n=1).apply(lambda l: ":".join(l[1:]))
b["Name_of_restaurant"] = b.Name_of_restaurant.str.split("'", n=1).apply(lambda l: ":".join(l[1:]))
b["Name_of_restaurant"] = b.Name_of_restaurant.str.split("'", n=1).apply(lambda l: ":".join(l[:1]))
b["Name_of_restaurant"]

#Cleaning and creation of "Text"
b["Text"] = b.lista.str.split("Text:", n=1).apply(lambda l: ":".join(l[1:]))
b["Text"] = b.Text.str.split("'", n=1).apply(lambda l: ":".join(l[1:]))
b["Text"] = b.Text.str.split("'", n=1).apply(lambda l: ":".join(l[1:]))
b["Text"]
