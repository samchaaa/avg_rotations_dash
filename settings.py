import os

class Settings:

    # Put the ID of your Google Sheet here:
    SHEET_ID = "1K9vDCK7kdn2yTwgq39fjAwDx_yvQQVXefOwMR9WHKmw"

    # Number of business days to gather and maintain history.
    DATE_RANGE = 5

    # Resamples ticks to this interval. Accepts "1Min", "15Min", "1H", etc. (any rules from pandas.DataFrame.resample).
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.resample.html
    INTERVAL = '5Min'

    # The interval to calculate moving averages of rotations.
    ROTATIONS_AVG = 20

    # Instrument names from Dukascopy. Note the name is the same, with any "." or "/" taken out.
    # https://www.dukascopy.com/swiss/english/marketwatch/historical/
    INSTS = """

    GBPUSD
    USA500IDXUSD
    BTCUSD


    """

    PATH = os.path.dirname(os.path.abspath(__file__))
    PATH_DATA = PATH + "/data"
    PATH_RESULTS = PATH + "/results"

    # Automatically takes the first .json file in your main directory for service file key.
    AUTH_PATH = PATH + "/" + [x for x in os.listdir(PATH) if '.json' in x][0]

