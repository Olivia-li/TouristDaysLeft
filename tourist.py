import json
from datetime import datetime
import requests

YOUR_API_KEY = "API KEY HERE"


def getPastYearFiles(date):
    lst = []
    date_object = datetime.strptime(date, '%m-%d-%Y').date()
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    for month in months[:date_object.month]:
        lst.append(f'Takeout/Location History/Semantic Location History/{date_object.year}/{date_object.year}_{month.upper()}.json')
    if len(lst) < 12:
        for month in months[date_object.month:]:
            lst.append(f'{date_object.year-1}/{date_object.year-1}_{month.upper()}.json')
    return lst

def cleanedData(file_names):
    lst = []
    for date in file_names:
        with open(date) as json_file:
            location_object = json.load(json_file)["timelineObjects"]
            for entry in location_object:
                if "placeVisit" in entry:
                    keys = ["location", "duration"]
                    entry['placeVisit'] = {key: entry['placeVisit'][key] for key in keys}
                    lst.append(entry)
    return lst

def removeHourlyData(entries):
    temp = int(entries[0]["placeVisit"]["duration"]["startTimestampMs"]) // 1000
    previous_date = datetime.fromtimestamp(temp)
    cleaned_list = []
    for item in entries[1:]:
        timestamp = item["placeVisit"]["duration"]["startTimestampMs"]
        timestamp = int(timestamp) // 1000
        date = datetime.fromtimestamp(timestamp)
        if date.hour != previous_date.hour or date.day != previous_date.day or date.month != previous_date.month or date.year != previous_date.year:
            cleaned_list.append(item)
            previous_date = date
    return cleaned_list


def getCountry(place_id, country_code):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?key={YOUR_API_KEY}&place_id={place_id}'
    response = requests.get(url)
    res = json.loads(response.text)
    if res["status"] == "OK":
        for entry in res['result']['address_components']:
            if entry["short_name"].lower() == country_code:
                return True
        return False


def entriesInAmerica(entries):
    lst = []
    progress = 0
    for entry in entries:
        place_id = entry["placeVisit"]["location"]["placeId"]
        progress += 1
        print(f'{round(progress/len(entries)*100, 2)}% complete!')
        if getCountry(place_id, "us"):
            lst.append(entry)
    return lst

def daysInAmerica(entries):
    temp = int(entries[0]["placeVisit"]["duration"]["startTimestampMs"])//1000
    previous_date = datetime.fromtimestamp(temp)
    cleaned_list = []
    for item in entries[1:]:
        timestamp = item["placeVisit"]["duration"]["startTimestampMs"]
        timestamp = int(timestamp) // 1000
        date = datetime.fromtimestamp(timestamp)
        if date.day != previous_date.day or date.month != previous_date.month or date.year != previous_date.year:
            cleaned_list.append(item)
            previous_date = date
    return cleaned_list

def getInput():
    date = input("Input your date in this format: MM-DD-YYYY \n")
    return date


if __name__ == "__main__":
    date = getInput()
    files = getPastYearFiles(date)
    entries_past_year = cleanedData(files)
    no_hour_repeats = removeHourlyData(entries_past_year)
    entries_in_America = entriesInAmerica(no_hour_repeats)
    days = daysInAmerica(entries_in_America)
    print(f'Days spent in the US: {len(days)}')
    print(f'Tourist Days left in the US: {182 - len(days)}')





