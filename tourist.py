import json
import sys
from datetime import datetime
import requests

YOUR_API_KEY =


def getPastYearFiles(date):
    lst = []
    date_object = datetime.strptime(date, '%m-%d-%Y').date()
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    for month in months[:date_object.month]:
        lst.append(f'{date_object.year}/{date_object.year}_{month.upper()}.json')
    if len(lst) < 12:
        for month in months[date_object.month:]:
            lst.append(f'{date_object.year-1}/{date_object.year-1}_{month.upper()}.json')
    return lst

def getCleanedData(file_names):
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
        if date.hour != previous_date.hour and date.day != previous_date.day or date.month != previous_date.month or date.year != previous_date.year:
            cleaned_list.append(item)
            previous_date = date
    return cleaned_list


def getCountry(place_id, country_code):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?key={YOUR_API_KEY}&place_id={place_id}'
    print(url)
    response = requests.get(url)
    res = json.loads(response.text)
    if res["status"] == "OK":
        for entry in res['result']['address_components']:
            if entry["short_name"].lower() == country_code:
                return True
        return False


def entrysInAmerica(entries):
    lst = []
    for entry in entries:
        place_id = entry["placeVisit"]["location"]["placeId"]
        if getCountry(place_id, "us"):
            lst.append(entry)
    return lst



a = getPastYearFiles("05-20-2020")
b= getCleanedData(a)
print(len(b))
print(b)
c = removeHourlyData(b)
print(len(c))
d = entrysInAmerica(b)
print(len(d))








#
# def getYearData(date):
#     lst = []
#     for entry in data_dictionary:
#         if int(entry["timestampMs"]) >= int(timeStamp):
#             lst.append(entry)
#     return lst
#
# def getDayData(lst):
    # temp = int(lst["timestampMs"])//1000
    # previous_date = datetime.fromtimestamp(temp)
    # cleaned_list = []
    # for item in lst[1:]:
    #     timestamp = item["timestampMs"]
    #     timestamp = int(timestamp) // 1000
    #     date = datetime.fromtimestamp(timestamp)
    #     print(date)
    #     if date.day != previous_date.day or date.month != previous_date.month or date.year != previous_date.year:
    #         cleaned_list.append(item)
    #         previous_date = date
    # return cleaned_list
#

#
# # if __name__ == "__main__":
# #     a = getDataAfter(sys.argv[0])
# #     b = entrysInAmerica(a)
# #     c = getDayData(b)
# #     print(f'Days spend in the US: {len(c)}')
# #     print(f'Tourist Days left in the US: {182 - len(c)}')
#
# a = getDataAfter(1588710148056)
# b = entrysInAmerica(a)
# c = getDayData(b)
# print(f'Days spend in the US: {len(c)}')
# print(f'Tourist Days left in the US: {182 - len(c)}')

