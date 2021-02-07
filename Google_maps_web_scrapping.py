# WEB SCRAPPING GOOGLE MAPS
# From coordinates, radius and keyword, it is possible to obtain all the places within this circle.

# Libraries 
import requests
import json
import time
import pandas as pd

# Data extraction
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


# To get the following number you have to sign up in Google Cloud Platform
api = GooglePlaces("AIzaSyAoxhDWppkYjOKNjelGF9uBbQPRme2t9Tw")

# Write coordinates of the place, radius and keyword
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

google_maps = pd.DataFrame({'lista': lista})

google_maps["lista"]

google_maps.to_csv("google_maps.csv")
