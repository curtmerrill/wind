# Wind

## Usage

Install the Python requirements.

    $ pip install -r requirements

Get a [Forecast.io API key](https://developer.forecast.io).

Edit the `API_KEY`, `COORDS`, and `DAYS_HISTORY` variables at the top of the script.

Run the script:

    $ python fetch_data.py

There should now be a file called `wind_data.csv` in your working directory.

## Notes

As configured, the script retrieves times in UTC.

If the `windSpeed` value is missing from the API results, that hour is skipped. When
I pulled in 365 days of data from May 23, 2015, to May 21, 2016, there were 13
missing hours (0.15%) Your mileage may vary.
