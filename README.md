# Tourist Days Left
Google maps is constantly tracking my location data and it's probably constantly tracking yours too! With all this data I decided to make a program that figures out how many of my 182 tourist days I have left in the year so I don't illegally overstay in the US and now you can too! Go Big Brother!!! 

## Download your location data from Google Maps
Go to [Google Takeout](https://takeout.google.com/settings/takeout) and check "Location History". Download your location data as a JSON file. 

## Installations and Setup
Cool, now that you have your data, install all the necessary stuffs needed to run this script. 
1) In your terminal `cd` into whatever directory you want to clone my repository and run `git clone https://github.com/Olivia-li/TouristDaysLeft.git`. 
2) We'll be using the Python modules `datetime`, `requests`. If you don't have these libraries installed run the following commands in your terminal: `pip install DateTime` and `pip install requests`
3) Go to [Google's "Get an API Key" guide](https://developers.google.com/places/web-service/get-api-key) and get yourself an API key
4) Open up `tourist.py` and you should see `YOUR_API_KEY = "API KEY HERE"` at the top of the file. Replace `"API KEY HERE"` with the API key that you got from the previous step. 
5) Find the "Takeout" folder that you downloaded from Google Takeout and pop that bad boy inside the repository folder

## Run the file
1) Nice! `cd` into the repository folder and run `python3 tourist.py` 
2) Input today's date in the following format `MM-DD-YYYY`
3) Wait until the progress says it's `100% complete`
4) Congrats you should get an output telling you how many days you have left to vacation in the US!
