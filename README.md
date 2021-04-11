# Days in America
Google maps is constantly tracking my location data and it's probably constantly tracking yours too! With all this data I made a program that determines how many of my 182 tourist days in the US I have left in the year so I don't illegally overstay and now you can too! 

Edit: I've rewritten the program in Crystal to more efficiently track how many days I've stayed in the US for tax purposes. The program checks to see how many days you've been in the United States within a given year. 

# Crystal Program (To track days within a given year for tax purposes)

## Get your location data
Go to [Google Takeout](https://takeout.google.com/settings/takeout) and check "Location History". Download your location data as a JSON file. 

## Installation and Setup
1) Clone my repo into whatever directly of your choosingCancel changes
2) Make sure you've installed crystal
3) Go to [Google's "Get an API Key" guide](https://developers.google.com/places/web-service/get-api-key) and get yourself an API key. 
4) run `echo API_KEY=your API key here >> .env.cr` inside of the directory you cloned the repo in
5) Place the yearly files directly into the repo directory. The yearly files should be located in `/Takeout/Location History/Semantic Location History/`

## Run the file
7) run `crystal tourist.cr` inside of your repo directory
8) Congrats you should get an output telling you how many days you have left to vacation in the US!


# Python Program (To track tourist days)

## Get your location data
Go to [Google Takeout](https://takeout.google.com/settings/takeout) and check "Location History". Download your location data as a JSON file. 

## Installation and Setup
Cool, now that you have your data, install all the necessary stuffs needed to run this script. 
1) In your terminal `cd` into whatever directory you want to clone my repository in and run `git clone https://github.com/Olivia-li/TouristDaysLeft.git`. 
2) We'll be using the Python modules `datetime`, `requests`. If you don't have these libraries installed run the following commands in your terminal: `pip install DateTime` and `pip install requests`
3) Go to [Google's "Get an API Key" guide](https://developers.google.com/places/web-service/get-api-key) and get yourself an API key
4) Open up `tourist.py` and you should see `YOUR_API_KEY = "API KEY HERE"` at the top of the file. Replace `"API KEY HERE"` with the API key that you got from the previous step. 
5) Find the "Takeout" folder that you downloaded from Google Takeout and pop that bad boy inside the repository folder

## Run the file
1) Nice! `cd` into the repository folder and run `python3 tourist.py` 
2) Input today's date in the following format `MM-DD-YYYY`
3) Wait until the progress says it's `100% complete`
4) Congrats you should get an output telling you how many days you have left to vacation in the US!
