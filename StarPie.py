# this tis the python scfript that actulaly finds out where all the bodies and stars are i guess it can be functional n its wnw but its more fun to let the bas script do the work for you;)
import swisseph as swe

def calculate_chart(date, time, latitude, longitude):
    swe.set_ephe_path('/path/to/ephemeris/files')  # specify the path to your ephemeris files

    # Convert date and time to Julian Day Number
    year, month, day = map(int, date.split('-'))
    hour, minute = map(int, time.split(':'))
    jd = swe.julday(year, month, day, hour + minute/60)

    # Get the positions of the planets and other celestial bodies
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

# Example usage:
calculate_chart('1999-02-09', '12:24', 31.7619, -106.4850)
