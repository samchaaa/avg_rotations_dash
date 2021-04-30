from urllib import request
from lzma import LZMADecompressor, LZMAError, FORMAT_AUTO
from urllib.error import HTTPError
import struct
from datetime import datetime, timedelta


def decompress_lzma(data):

    results = []

    while True:
        decomp = LZMADecompressor(FORMAT_AUTO, None, None)
        try:
            res = decomp.decompress(data)
        except LZMAError:
            if results:
                break
            else:
                raise
        results.append(res)
        data = decomp.unused_data
        if not data:
            break
        if not decomp.eof:
            raise LZMAError("Compressed data ended before the end-of-stream marker was reached")

    return b"".join(results)


def normalize_tick(symbol, day, time, ask, bid, ask_vol, bid_vol):

    date = day + timedelta(milliseconds=time)

    if any(map(lambda x: x in symbol.lower(), ['usdrub', 'xagusd', 'xauusd', 'jpy', 'usatechidxusd', 'usa500idxusd'])):
        point = 1000
    elif any(map(lambda x: x in symbol.lower(), ['btcusd'])):
        point = 10
    else:
        point = 100000

    return [date, ask/point, bid/point, round(ask_vol * 1000000), round(bid_vol * 1000000)]


def tokenize(buffer):

    token_size = 20
    token_count = int(len(buffer) / token_size)
    tokens = list(map(lambda x: struct.unpack_from('>3I2f', buffer, token_size * x), range(0, token_count)))

    return tokens


def download_ticks(symbol, day):

    url_prefix = 'https://datafeed.dukascopy.com/datafeed'
    ticks_day = []

    end_hour = 24

    if datetime.utcnow().date() == day:
        end_hour = datetime.utcnow().hour-1
    else:
        pass

    for h in range(0, end_hour):
        file_name = f'{h:02d}h_ticks.bi5'
        url = f'{url_prefix}/{symbol}/{day.year:04d}/{day.month-1:02d}/{day.day:02d}/{file_name}'
        print(f'downloading: {url}')
        req = request.Request(url)
        try:
            with request.urlopen(req) as res:
                res_body = res.read()
        except HTTPError:
            print('download failed. continuing..')
            continue
        if len(res_body):
            try:
                data = decompress_lzma(res_body)
            except LZMAError:
                print('decompress failed. continuing..')
                continue
        else:
            data = []
        tokenized_data = tokenize(data)
        ticks_hour = list(map(lambda x: normalize_tick(symbol, day + timedelta(hours=h), *x), tokenized_data))
        ticks_day.extend(ticks_hour)

    return ticks_day


def format_to_csv_for_ticks(ticks):
    return '\n'.join(map(lambda x: '{},{},{},{},{}'.format(x[0].strftime('%Y-%m-%d %H:%M:%S.%f'), *x[1:]), ticks))+'\n'


def main(symbol, start, end, dest):

    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(end, '%Y-%m-%d')
    output_dir = dest
    output_csv = f'{output_dir}/{symbol}_{start_date.strftime("%Y-%m-%d")}_{end_date.strftime("%Y-%m-%d")}.csv'

    d = start_date
    with open(output_csv, 'w') as f:
        while d <= end_date:
            ticks_day = download_ticks(symbol, d)
            f.write(format_to_csv_for_ticks(ticks_day))
            d += timedelta(days=1)

