require "./.env.cr"
require "json"
require "http/client"
require "time"

file_path = "2021/2021_APRIL.json"

def clean_data(file_path)
  cleaned_locations = [] of JSON::Any
  json = File.open(file_path)
  file = JSON.parse(json)
  file["timelineObjects"].as_a.each do |event|
    if event["placeVisit"]?
      cleaned_locations.push(event["placeVisit"])
    end
  end
  return cleaned_locations.map { |c| [c["location"]["placeId"].to_s, c["duration"]["startTimestampMs"].to_s] }.sort { |a, b| a[1] <=> b[1] }
end

def placeid_to_country(place_id)
  response = HTTP::Client.get "https://maps.googleapis.com/maps/api/place/details/json?key=#{API_KEY}&place_id=#{place_id}"
  json = JSON.parse(response.body.to_s)["result"]["address_components"]
  state = ""
  country = ""
  json.as_a.each do |area|
    if area["types"][0] == "administrative_area_level_1"
      state = area["long_name"]
    elsif area["types"][0] == "country"
      country = area["long_name"]
    end
  end
  puts [state, country]
  return [state, country]
end

def get_num_days(file_path)
  count = 0
  locations = clean_data(file_path)
  current_day = 0
  already_in_states = false
  locations.each do |place|
    if Time.unix_ms(place[1].to_i64).day != current_day && !already_in_states
      if placeid_to_country(place[0])[1] == "United States"
        count += 1
        already_in_states = true
      else
        already_in_states = false
      end
    end
  end
  return count
end
