import sqlite3
import folium

# Connect to the SQLite database
conn = sqlite3.connect('dorms.db')
cursor = conn.cursor()

# Coordinates of your workplace
workplace_lat = 33.76826203508398
workplace_lng = 55.421278481565906
radius_km = 20  # Radius in kilometers

# Query to fetch male dormitories within the specified radius
query = '''
WITH haversine AS (
    SELECT id,
           title,
           lat,
           lng,
           gender,
           6371 * 2 * ASIN(SQRT(
               POWER(SIN((? - lat) * PI() / 180 / 2), 2) +
               COS(? * PI() / 180) * COS(lat * PI() / 180) *
               POWER(SIN((? - lng) * PI() / 180 / 2), 2)
           )) AS distance
    FROM dorms
)
SELECT id,
       title,
       lat,
       lng,
       distance
FROM haversine
WHERE distance <= ? AND gender = 'Male'
ORDER BY distance;
'''

# Execute the query with parameters
cursor.execute(query, (workplace_lat, workplace_lat, workplace_lng, radius_km))
nearby_dorms = cursor.fetchall()

# Create a map centered around your workplace
mymap = folium.Map(location=[workplace_lat, workplace_lng], zoom_start=13)

# Add a marker for the workplace
folium.Marker(
    [workplace_lat, workplace_lng],
    popup="Your Workplace",
    icon=folium.Icon(color="red")
).add_to(mymap)

# Add markers for each nearby dormitory
for dorm in nearby_dorms:
    dorm_id, title, lat, lng, distance = dorm
    folium.Marker(
        [lat, lng],
        popup=f"{title}\nDistance: {distance:.2f} km",
        icon=folium.Icon(color="blue")
    ).add_to(mymap)

# Save the map to an HTML file
mymap.save("nearby_dorms_map.html")

# Print message
print("Map with nearby male dormitories saved to 'nearby_dorms_map.html'.")

# Close the connection
conn.close()
