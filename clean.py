import os
import pandas as pd
from datetime import datetime
from settings import Settings


def get_all(inst):

    # concat all .csvs within dir
    data = pd.DataFrame()

    files = [
        file for file
        in os.listdir('{}/{}'.format(Settings.PATH_DATA, inst))
        if os.path.getsize('{}/{}/{}'.format(Settings.PATH_DATA, inst, file)) > 2
    ]

    for csv in files:
        data = pd.concat([
            data,
            pd.read_csv(
                '{}/{}/{}'.format(Settings.PATH_DATA, inst, csv),
                header=None
            )
        ])
    data.columns = ['dt', 'bid', 'ask', 'bidvol', 'askvol']

    return data


def clean(inst, interval):

    data = get_all(inst)
    data = data.drop_duplicates()
    data['mid'] = (data['bid'] + data['ask']) / 2
    data.index = data['dt'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f'))
    data = data[['mid']].resample(interval).ohlc()

    return data