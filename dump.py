from datetime import datetime
from pandas.tseries.offsets import BDay
import os
import re
from settings import Settings


# check if data is older than DATE_RANGE (business days), if so delete
def dump_data():

    for inst in os.listdir(Settings.PATH_DATA):
        for file in os.listdir('{}/{}'.format(Settings.PATH_DATA, inst)):
            file_dt = datetime.strptime(re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', file).group(0), '%Y-%m-%d').date()
            min_dt = (datetime.utcnow().date() - BDay(Settings.DATE_RANGE)).date()
            if file_dt < min_dt:
                print('deleting {}'.format(file))
                os.remove('{}/{}/{}'.format(Settings.PATH_DATA, inst, file))
