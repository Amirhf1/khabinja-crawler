import requests
import sqlite3
import json

# Step 1: Request the API URL
url = "https://api.khabinja.com/v1/general/dorms/near_dorms?lat=35.7228166912126&lng=51.31368291976048&radius=20"
response = requests.get(url)
data = response.json()

# Step 3: Define the SQLite Database Structure
conn = sqlite3.connect('dorms.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS dorms (
    id INTEGER PRIMARY KEY,
    title TEXT,
    slug TEXT,
    gender TEXT,
    min_price TEXT,
    tel_status TEXT,
    description TEXT,
    status_description TEXT,
    address TEXT,
    capacity TEXT,
    lat REAL,
    lng REAL,
    tel TEXT,
    main_image TEXT,
    comment_count INTEGER,
    average_score REAL,
    payment_expired_at TEXT,
    expire_order_time TEXT,
    created TEXT,
    updated TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS features (
    dorm_id INTEGER,
    feature_id INTEGER,
    title TEXT,
    FOREIGN KEY(dorm_id) REFERENCES dorms(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS images (
    dorm_id INTEGER,
    image_id INTEGER,
    path TEXT,
    width INTEGER,
    height INTEGER,
    is_link TEXT,
    type TEXT,
    format TEXT,
    size TEXT,
    FOREIGN KEY(dorm_id) REFERENCES dorms(id)
)
''')

# Step 4: Insert Data into the Database
for dorm in data['data']:
    cursor.execute('''
    INSERT INTO dorms (id, title, slug, gender, min_price, tel_status, description, status_description, address, capacity, lat, lng, tel, main_image, comment_count, average_score, payment_expired_at, expire_order_time, created, updated)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        dorm['id'], dorm['title'], dorm['slug'], dorm['gender'], dorm['min_price'], dorm['tel_status'], dorm['description'], dorm['status_description'],
        dorm['address'], dorm['capacity'], float(dorm['lat']), float(dorm['lng']), json.dumps(dorm.get('tel', [])), dorm.get('main_image', {}).get('path'),
        dorm.get('comment', {}).get('count', 0), dorm.get('comment', {}).get('average_score', 0), dorm['payment_expired_at'], dorm['expire_order_time'], dorm['created'], dorm['updated']
    ))

    for feature in dorm.get('features', []):
        cursor.execute('''
        INSERT INTO features (dorm_id, feature_id, title)
        VALUES (?, ?, ?)
        ''', (dorm['id'], feature['id'], feature['title']))

    for image in dorm.get('files', []):
        cursor.execute('''
        INSERT INTO images (dorm_id, image_id, path, width, height, is_link, type, format, size)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dorm['id'], image['id'], image['path'], int(image['width']), int(image['height']), image['is_link'], image['type'], image['format'], image['size']
        ))

# Commit the transaction
conn.commit()
conn.close()

print("Data has been successfully fetched and stored in the SQLite database.")
