#!/usr/env/bin python

import csv
import os
import requests
from datetime import datetime, timedelta

API_KEY = open(os.path.expanduser('~/.api-keys/forecast.io'), 'r').read().strip()
API_URL = "https://api.forecast.io/forecast/{api_key}/{lat},{lon},{timestamp}"

MANTEO_COORDS = [35.908199, -75.668230]

DAYS_HISTORY = 365

with open('wind_data.csv', 'w') as csv_file:
    fieldnames = [
        'posix_time',
        'year',
        'month',
        'day',
        'hour',
        'wind_direction',
        'wind_speed',
    ]

    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for days_ago in range(0-DAYS_HISTORY,0):
        day = datetime.utcnow() - timedelta(days=days_ago)
        response = requests.get(API_URL.format(
            api_key=API_KEY,
            lat=MANTEO_COORDS[0],
            lon=MANTEO_COORDS[1],
            timestamp=day.replace(second=0, microsecond=0).isoformat()+'Z'
        ))
        if response.status_code != 200:
            print("ERROR fetching data for {}".format(day.strftime("%Y/%m/%d")))
        else:
            for hour in response.json()['hourly']['data']:
                dt = datetime.fromtimestamp(hour['time'])
                writer.writerow({
                    'posix_time': hour['time'],
                    'year': dt.year,
                    'month': dt.month,
                    'day': dt.day,
                    'hour': dt.hour,
                    'wind_direction': hour['windBearing'],
                    'wind_speed': hour['windSpeed']
                })
                    

