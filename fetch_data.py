#!/usr/env/bin python

import csv
import os
import requests
from datetime import datetime, timedelta

API_KEY = open(os.path.expanduser('~/.api-keys/forecast.io'), 'r').read().strip()
COORDS = [35.908199, -75.668230]
DAYS_HISTORY = 365

API_URL = "https://api.darksky.net/forecast/{api_key}/{lat},{lon},{timestamp}"

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

    for days_ago in range(1, DAYS_HISTORY+1):
        day = datetime.utcnow() - timedelta(days=days_ago)
        response = requests.get(API_URL.format(
            api_key=API_KEY,
            lat=COORDS[0],
            lon=COORDS[1],
            timestamp=day.replace(second=0, microsecond=0).isoformat()+'Z'
        ))
        if response.status_code != 200:
            print("ERROR fetching data for {}".format(day.strftime("%Y/%m/%d")))
        else:
            for hour in response.json()['hourly']['data']:
                dt = datetime.fromtimestamp(hour['time'])

                try:
                    if int(hour['windSpeed']) == 0:
                        wind_direction = ''
                    else:
                        wind_direction = hour['windBearing']

                    writer.writerow({
                        'posix_time': hour['time'],
                        'year': dt.year,
                        'month': dt.month,
                        'day': dt.day,
                        'hour': dt.hour,
                        'wind_direction': wind_direction,
                        'wind_speed': hour['windSpeed'],
                    })
                except KeyError:
                    pass

