import json
import sys
from datetime import datetime
from geopy.geocoders import Nominatim


with open('history.json') as json_file:
    data = json.load(json_file)

def getDataAfter(timeStamp):
    lst = []
    for entry in data:
        if int(entry["timestampMs"]) >= timeStamp:
            lst.append(entry)
    return lst

def getDayData(lst):
    temp = int(lst[0]["timestampMs"])//1000
    previous_date = datetime.fromtimestamp(temp)
    cleaned_list = []
    for item in lst[1:]:
        timestamp = item["timestampMs"]
        timestamp = int(timestamp) // 1000
        date = datetime.fromtimestamp(timestamp)
        if date.day != previous_date.day or date.month != previous_date.month or date.year != previous_date.year:
            cleaned_list.append(item)
            previous_date = date
    return cleaned_list

def entrysInAmerica(lst):
    return_list = []
    for entry in lst:
        latitude = int(entry["latitudeE7"])/10**7
        longitude = int(entry["longitudeE7"])/10**7
        geolocator = Nominatim(user_agent="My Tourist Days")
        location = geolocator.reverse(f'{latitude}, {longitude}')
        location_country = location.raw["address"]["country_code"]
        if location_country.lower() == "us":
            return_list.append(entry)
    return return_list

if __name__ == "__main__":
    a = getDataAfter(sys.argv[1])
    b = entrysInAmerica(a)
    c = getDayData(b)
    print(f'Days spend in the US: {len(c)}')
    print(f'Tourist Days left in the US: {182 - len(c)}')
