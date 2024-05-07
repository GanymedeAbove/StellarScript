import swisseph as swe
import sys
import requests

def get_coordinates(city_name, api_key):
    """Use the OpenCage Geocode API to get coordinates based on the city name."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city_name}&key={api_key}&limit=1"
    response = requests.get(url)
    if response.status_code != 200:
        print("Error fetching geocoding data")
        return None, None
    data = response.json()
    if data['results']:
        lat = data['results'][0]['geometry']['lat']
        lon = data['results'][0]['geometry']['lng']
        return lat, lon
    else:
        print("No results found for the specified city")
        return None, None

def calculate_chart(date, time, city_name, api_key):
    latitude, longitude = get_coordinates(city_name, api_key)
    if latitude is None or longitude is None:
        return  # Exit if geocoding fails

    swe.set_ephe_path('./ephemeris')  # Adjusted to a relative path

    # Convert date and time to Julian Day Number
    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))
    jd = swe.julday(year, month, day, hour + minute/60)

    # Define celestial bodies to calculate positions
    bodies = ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN', 'URANUS', 'NEPTUNE', 'PLUTO', 'TRUE_NODE']
    positions = {}
    for body in bodies:
        body_id = getattr(swe, body)
        position = swe.calc(jd, body_id)
        positions[body] = {
            'longitude': position[0],
            'latitude': position[1],
            'distance': position[2],
            'speed': position[3],
            'is_retrograde': 'Retrograde' if position[3] < 0 else 'Direct'
        }

    # Print results
    print("Planetary Positions:")
    for body, data in positions.items():
        print(f"{body}: {data['longitude']}°, {data['latitude']}°, {data['distance']} AU, {data['speed']}°/day, {data['is_retrograde']}")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        date, time, city_name, api_key = sys.argv[1:5]
        calculate_chart(date, time, city_name, api_key)
    else:
        print("Usage: python StarPie.py <date> <time> <city name> <API key>")
