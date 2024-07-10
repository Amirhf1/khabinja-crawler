# Nearby Dormitories Map

This project retrieves dormitory data from an SQLite database and displays dormitories within a specified radius around a given location on an interactive map. The dormitories can be filtered by gender and minimum score.

## Prerequisites

- Python 3.x
- SQLite database with dormitory data
- The following Python packages:
  - `sqlite3`
  - `folium`

## Installation

1. **Clone the repository** (if applicable):
   ```sh
   git clone git@github.com:Amirhf1/khabinja-crawler.git && 
   cd khabinja-crawler
   
2. **Set up a virtual environment (optional but recommended):**
   ```sh
    python3 -m venv venv
   ```

   ```sh
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
   ```
4. run main 
```sh
    python3 main.py
```
5. run distance 
```sh
    python3 distance.py
```
**Configuration `distance.py`**

Modify the following parameters in the distance.py script as needed:

workplace_lat: Latitude of your workplace.

workplace_lng: Longitude of your workplace.

radius_km: Radius in kilometers to search for nearby dormitories.

gender: Gender filter for dormitories (e.g., 'Male', 'Female').

min_score: Minimum average score filter for dormitories.



