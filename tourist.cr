require "./.env.cr"
require "json"
require "http/client"

directory_years = ["./2020", "./2019"]
test_dir = ["./2021"]

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
  response = HTTP::Client.get "https://maps.googleapis.com/maps/api/place/details/json?key=#{API_KEY}&place_id=#{place_id}&fields=address_component"
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

def get_days_in_file(file_path)
  count = 0
  locations = clean_data(file_path)
  current_day = 0
  locations.each do |place|
    if Time.unix_ms(place[1].to_i64).day != current_day
      puts Time.unix_ms(place[1].to_i64).day
      current_day = Time.unix_ms(place[1].to_i64).day
      if placeid_to_country(place[0])[1] == "United States"
        count += 1
      end
    end
  end
  return count
end

def get_days_in_year(dir_path)
  dir = Dir.open(dir_path)
  count = 0
  dir.each_child do |month|
    count += get_days_in_file("#{dir_path}/#{month.to_s}")
  end
  return count
end
