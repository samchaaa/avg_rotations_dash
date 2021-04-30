# Avg Rotation Dash

Avg Rotation Dash is a dashboard showing statistics of "rotations" for different financial instruments. It is mainly for manual intraday and algorithmic traders.

The point of measuring rotations of a market is to give us reasonable expectations of risk (in distance terms).

Avg Rotation Dash downloads free tick data from Dukascopy, then runs calculations resampling the ticks and measuring rotations. Results are written to Google Sheets, the stats and visualizations may be further customized. 

The script may be run or scheduled locally, or hosted in the cloud (using services such as PythonAnywhere, GCP, or AWS).

[preview pic]

[Corresponding Medium article](link).

[Corresponding YouTube video](link).

The idea of measuring rotations originally came from FT71 (FuturesTrader71):
[Vimeo - Harmonic Rotations](https://vimeo.com/145456969)


The code for downloading ticks from Dukascopy came originally from the following repos:
[terukusu / download-tick-from-dukascopy](https://github.com/terukusu/download-tick-from-dukascopy)
[giuse88 / duka](https://github.com/giuse88/duka)


Also thanks to [Make a README](https://www.makeareadme.com/).


## Installation

1. **"File" > "Make a copy" of [this Google Sheet](https://docs.google.com/spreadsheets/d/1Ur7CJJu-cDkhcFjEXG4smsxlKYc_323PcPYloLEvshA/edit#gid=0)**

2. **Download this repo and unzip to where you'll be running it (local, PythonAnywhere, AWS, et cetera).** 

3. **Run `pip install gspread`**

4. **Get service account credentials for Google Sheets:**
   - Create a [new project in Google Cloud Console](https://console.cloud.google.com/projectcreate).
   - [Enable Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com).
   - [Enable Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com).
   - [Create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts/create) (name it and click through rest of options).
   - Once you're back on the credentials page, click on "Service Account". Click "Keys". Click "Add key". Click "Create new key". Select JSON (the default) and it will download.

      [(Instructions for steps 1-5 from gspread docs)](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account).
   - Click and drag the JSON into to your repo folder (just inside the main folder).
   - Share the Google Sheet you copied with this service account e-mail.
   

5. **In the main repo folder, go into `settings.py` and adjust your settings as needed (explained below).**

## Settings

In `settings.py`:

**SHEET_ID** *(required)*: Id of the Google Sheet you copied. Looks like "1Ur7CJJu-cDkhcFjEXG4smsxlKYc_323PcPYloLEvshA".

**DATE_RANGE** *(default 5)*: Number of business days to download data. Days outside of this will be deleted (to manage storage).

**INTERVAL** *(default '5Min')*: Ticks will be resampled to this time period. Accepts rules such as "1Min", "1H", or anything from [pandas.DataFrame.resample](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html). Higher timeframes will give you higher level swings, but less data points. I prefer 1Min or 5Min for consistent results.

**ROTATIONS_AVG** *(default 10)*: Periods for a moving average over the rotation results. Displays in the Sheet as a chart, and a single number (average of last 10 rotations).

**INSTS** *(default GBPUSD, USA500IDXUSD, BTCUSD)*: This is a multi-line string, just add somewhere in the string and the script will parse it. Uses names from [Dukascopy](https://www.dukascopy.com/swiss/english/marketwatch/historical/), without the "." or "/"'s.

## Usage

Run locally:

```python
python run_all.py
```

Schedule in PythonAnywhere:

```
python3.6 /home/samcha/avg-rot-dash/run_all.py
```

## Troubleshooting

If you are having issues, it may be due to the scaling that happens converting the ticks from binary (this happens in `download_dukas.py`). If you're downloading an obscure instrument, it may not be handled in `normalize_tick`.

Scaling also occurs for *JPY and other fx instruments, in `rotations.py`. Again, if you're looking at obscure instruments you may handle scaling in this file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)