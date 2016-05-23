# Wind

Where would you end up if you traveled based on the direction and strength of 
wind in your hometown?

Using the Forecast.io API, I downloaded 365 days of hourly wind data
(wind direction and speed, in miles per hour).

For each reading, I moved in the direction of the wind for a distance
equal to the wind speed. 

For example, if the reading showed 10 miles per hour bearing 25 degrees, I
would move 10 miles SSW (205 degrees).

(Wind directions are based on where the wind is coming from, so wind bearing
25 degrees is blowing from 25 degrees toward 205 degrees.)

Here is the [resulting GeoJSON](https://gist.github.com/anonymous/59cc3a1712c3d0d671654f4cc207432c), which GitHub helpfully plots.
The GeoJSON is grouped by day, so you can click on a segment and see the date.

It gets weird near the poles. Let's say you're 5 miles from the North Pole.
If you face north and walk 10 miles straight ahead, you'll end up on the
other side of the planet, 5 miles from the pole.
But, chances are, if the wind was blowing north an hour ago, it's still blowing 
mostly north. So instead of continuing in the same direction you're facing 
(south), you have to turn around and go back towards the pole.


## Usage

Install the Python requirements.

    $ pip install -r requirements.txt

Get a [Forecast.io API key](https://developer.forecast.io).

Edit the `API_KEY`, `COORDS`, and `DAYS_HISTORY` variables at the top of the script.

Run the script:

    $ python fetch_data.py

There should now be a file called `wind_data.csv` in your working directory.

Now run `csv2json.py` to generate a GeoJSON:

    $ python csv2geojson.py

There should now be a file called `wind_data.json` in your working directory. 


## Notes

As configured, the script retrieves times in UTC.

If the `windSpeed` value is missing from the API results, that hour is skipped. When
I pulled in 365 days of data from May 23, 2015, to May 21, 2016, there were 13
missing hours (0.15%) Your mileage may vary.
