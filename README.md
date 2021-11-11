# Avg Rotation Dash

[![Google Sheet](https://github.com/samchaaa/avg_rotations_dash/raw/main/preview.png)](https://docs.google.com/spreadsheets/d/1Ur7CJJu-cDkhcFjEXG4smsxlKYc_323PcPYloLEvshA/edit#gid=0)
[Google Sheet - Average Rotations Dashboard LIVE](https://docs.google.com/spreadsheets/d/1Ur7CJJu-cDkhcFjEXG4smsxlKYc_323PcPYloLEvshA/edit#gid=0)

Note: As of Nov 2021, this will be scheduled to run just 1x per day to save resources. 

Avg Rotation Dash is a dashboard showing statistics of "rotations" for different financial instruments. It is mainly for manual intraday and algorithmic traders.

The point of measuring rotations is to give us reasonable (but dynamic) expectations of risk.

Avg Rotation Dash downloads free tick data from Dukascopy, then resamples the ticks and measures rotations. Results are written to Google Sheets, where stats and visualizations may be further customized. 

The script can run or be scheduled locally, or hosted in the cloud (using services such as PythonAnywhere, GCP, or AWS).

[Hacker Noon article](https://hackernoon.com/adjust-your-market-risk-wisely-with-this-awesome-python-and-google-sheets-rotation-dashboard-3n1e34l1)

[YouTube video](https://github.com/samchaaa/avg_rotations_dash/)

The idea of measuring rotations originally came from FT71 (FuturesTrader71):

[Vimeo - Harmonic Rotations](https://vimeo.com/145456969)


The code for downloading ticks from Dukascopy came originally from these repos:

[terukusu / download-tick-from-dukascopy](https://github.com/terukusu/download-tick-from-dukascopy)

[giuse88 / duka](https://github.com/giuse88/duka)


Also thanks to:

[Make a README](https://www.makeareadme.com/)

[Ultraworking - Work Marathon](https://www.ultraworking.com/work-marathon)


## Installation

1. **"File" > "Make a copy" of [this Google Sheet](https://docs.google.com/spreadsheets/d/1Ur7CJJu-cDkhcFjEXG4smsxlKYc_323PcPYloLEvshA/edit#gid=0)**

2. **Download and unzip this repo to where you'll run it (local, PythonAnywhere, AWS, et cetera).** 

3. **Run `pip install gspread`**

4. **Get service account credentials for Google Sheets:**
   - Create a [new project in Google Cloud Console](https://console.cloud.google.com/projectcreate).
   - [Enable Drive API](https://console.cloud.google.com/apis/library/drive.googleapis.com).
   - [Enable Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com).
   - [Create a service account](https://console.cloud.google.com/iam-admin/serviceaccounts/create) (name it and click through rest of options).
   - Once you're back on the credentials page, click "Service Account" > "Keys" > "Add key" > "Create new key". Select JSON (default) and it will download. Copy the service account e-mail.

      [(Instructions for steps 1-5 from gspread docs)](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account).
   - Click and drag the JSON credentials into to your repo folder (just inside the main folder, the script will find it automatically).
   - Share your Google Sheet with the service account e-mail (as editor).
   

5. **In the main repo folder, open `settings.py` to adjust your settings (explained below).**

## Settings

In `settings.py`:

**SHEET_ID** *(required)*: Id of the Google Sheet you copied. Looks like "1Ur7CJJu-cDkhcFjEXG4smsxlKYc_323PcPYloLEvshA".

**DATE_RANGE** *(default 5)*: Number of business days to download data. Days outside of this will be deleted (to manage storage).

**INTERVAL** *(default '5Min')*: Ticks will be resampled to this time period. Accepts rules such as "1Min", "1H", or anything from [pandas.DataFrame.resample](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html). Higher timeframes will give you higher level swings, but less data points.

**ROTATIONS_AVG** *(default 20)*: Periods for moving average over rotation results. Displays in the Sheet as a chart, and a single number (average of last 20 rotations).

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

If you are having issues, it may be due to the script not handling scaling for every single instrument that exists. This happens converting the ticks from binary (in `download_dukas.py`). If you're downloading an obscure instrument, edit `normalize_tick()` to handle it.

Scaling also occurs for *JPY and other fx instruments, in `rotations.py`. Again, if you're looking at obscure instruments you may handle scaling in this file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
