import swisseph as swe
import sys

def calculate_chart(date, time, latitude, longitude):
    # Use a relative path for the ephemeris files assuming they're in the same directory or specify dynamically
    swe.set_ephe_path('./ephemeris')  # Adjusted to a relative path

    try:
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

        # Calculate house cusps, Ascendant, and Midheaven
        house_system = 'P'  # Placidus system
        cusps, ascmc = swe.houses(jd, latitude, longitude, house_system.encode())
        houses = {f"House {i}": cusps[i] for i in range(1, 13)}
        ascendant = ascmc[0]
        midheaven = ascmc[1]

        # Print results
        print("Planetary Positions:")
        for body, data in positions.items():
            print(f"{body}: {data['longitude']}°, {data['latitude']}°, {data['distance']} AU, {data['speed']}°/day, {data['is_retrograde']}")

        print("\nHouse Cusps (Placidus):")
        for house, cusp in houses.items():
            print(f"{house}: {cusp}°")

        print(f"\nAscendant: {ascendant}°")
        print(f"Midheaven: {midheaven}°")

    except Exception as e:
        print(f"An error occurred: {e}")

# Use command-line arguments to pass parameters
if __name__ == "__main__":
    if len(sys.argv) == 5:
        date, time, lat, lon = sys.argv[1:5]
        calculate_chart(date, time, float(lat), float(lon))
    else:
        print("Usage: python StarPie.py <date> <time> <latitude> <longitude>")
