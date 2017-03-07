#!/usr/env/bin python

import csv
import os
import requests

from datetime import datetime, timedelta
from pytz import timezone

API_KEY = open(os.path.expanduser('~/.api-keys/forecast.io'), 'r').read().strip()
COORDS = [35.908199, -75.668230]
START_DATE = datetime(2016, 1, 1)
END_DATE = datetime(2016, 12, 31)
DAYS_HISTORY = 365

API_URL = "https://api.darksky.net/forecast/{api_key}/{lat},{lon},{timestamp}?exlude=currently,daily,flags"

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

    day = START_DATE
    while day <= END_DATE:
        response = requests.get(API_URL.format(
            api_key=API_KEY,
            lat=COORDS[0],
            lon=COORDS[1],
            timestamp=day.strftime('%Y-%m-%dT00:01:00')
        ))
        if response.status_code != 200:
            print("ERROR fetching data for {}".format(day.strftime("%Y/%m/%d")))
        else:
            response_tz = timezone(response.json()['timezone'])

            for hour in response.json()['hourly']['data']:
                dt = datetime.fromtimestamp(hour['time'])
                dt.replace(tzinfo=response_tz)

                try:
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

        day = day + timedelta(days=1)

