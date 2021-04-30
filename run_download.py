from download_dukas import main
from datetime import datetime, timedelta
import re
from pandas.tseries.offsets import BDay
import os
from settings import Settings


def check_max(inst):

    # Returns min/max date from current data by finding min/max filename (doesn't account for data within .csv)

    files = [
        file for file
        in os.listdir('{}/{}'.format(Settings.PATH_DATA, inst))
        if os.path.getsize('{}/{}/{}'.format(Settings.PATH_DATA, inst, file)) > 2
    ]

    if files:
        inst_max = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', max(files)).group(0)
        inst_min = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', min(files)).group(0)

    else:
        inst_min = False
        inst_max = False

    return inst_min, inst_max


def check_current(inst):

    # check current date against last updated date for all inst's

    inst_min, inst_max = check_max(inst)
    utcnow = datetime.utcnow().date()

    if all([inst_min, inst_max]):

        # Checking start date
        # If min < than this, you're good.
        if datetime.strptime(inst_min, '%Y-%m-%d').date() < (utcnow - BDay(Settings.DATE_RANGE)).date():
            pass

        # Else, download from this to whereever the min was.
        else:
            to_download_start = datetime.strftime((utcnow - BDay(Settings.DATE_RANGE)).date(), '%Y-%m-%d')
            to_download_end = inst_min
            download(inst, to_download_start, to_download_end)

        to_download_start = inst_max
        to_download_end = datetime.strftime(utcnow, '%Y-%m-%d')
        download(inst, to_download_start, to_download_end)

    else:
        to_download_start = datetime.strftime((utcnow - BDay(Settings.DATE_RANGE)).date(), '%Y-%m-%d')
        to_download_end = datetime.strftime(utcnow, '%Y-%m-%d')
        download(inst, to_download_start, to_download_end)

    return


def download(inst, start_date, end_date):

    # given start and end date, download each inst a day at a time

    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    diff = (end_dt - start_dt).days
    date_list = [datetime.strftime(end_dt - timedelta(days=x), '%Y-%m-%d') for x in range(0, diff+1)]
    print(start_dt, end_dt, diff, date_list)

    for date in date_list:
        main(inst, date, date, '{}/{}'.format(Settings.PATH_DATA, inst))

