from csv import DictReader
from datetime import date
from geojson import dumps, FeatureCollection, Feature, LineString
from geopy import Point
from geopy.distance import distance
from operator import itemgetter


# Load data into list of dictionaries

wind_data = []

with open('wind_data.csv') as csv_file:
    reader = DictReader(csv_file)
    for row in reader:
        wind_data.append(row)


# Sort data by timestamp

wind_data = sorted(wind_data, key=itemgetter('posix_time'))

current_date = date.today()
current_location = Point(35.908199, -75.668230)
current_feature = 'First Feature'
all_features = []

for record in wind_data:
    rdate = date(int(record['year']), int(record['month']), int(record['day']))
    if rdate != current_date:
        if current_feature != 'First Feature':
            all_features.append(current_feature)

        current_feature = Feature(
            geometry=LineString([ (current_location[1], current_location[0]) ]),
            properties={ 'date': rdate.strftime('%B %d, %Y') }
        )

        current_date = rdate

    wind_speed = float(record['wind_speed'])
    wind_dir = record['wind_direction']
    if wind_dir != '':
        bearing = (int(wind_dir) + 180) % 360
    else:
        bearing = 0

    next_location = distance(miles=wind_speed).destination(current_location, bearing)
    current_feature['geometry']['coordinates'].append([next_location[1], next_location[0]])

    current_location = next_location

all_features.append(current_feature)

feature_collection = FeatureCollection(all_features)

with open('wind_data.json','w') as json_file:
    json_file.write(dumps(feature_collection))

