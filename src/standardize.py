# Standard columns
STANDARD_COLS = ['date', 'symbol', 'series', 'isin',
                 'open', 'high', 'low', 'close', 'last', 'prev_close',
                 'volume', 'value', 'trades', 'fmt']




map_format1 = {
    'SYMBOL' : 'symbol',
    'SERIES' : 'series',
    'OPEN' : 'open',
    'HIGH' : 'high',
    'LOW' : 'low',
    'CLOSE' : 'close',
    'LAST' : 'last',
    'PREVCLOSE' : 'prev_close',
    'TOTTRDQTY' : 'volume',
    'TOTTRDVAL' : 'value',
    'TIMESTAMP' : 'date'
}

map_format2 = {
    'SYMBOL' : 'symbol',
    'SERIES' : 'series',
    'ISIN' : 'isin',
    'OPEN' : 'open',
    'HIGH' : 'high',
    'LOW' : 'low',
    'CLOSE' : 'close',
    'LAST' : 'last',
    'PREVCLOSE' : 'prev_close',
    'TOTTRDQTY' : 'volume',
    'TOTTRDVAL' : 'value',
    'TOTALTRADES': 'trades',
    'TIMESTAMP' : 'date'
}

map_format3 = {
    'TckrSymb' : 'symbol',
    'SctySrs' : 'series',
    'ISIN' : 'isin',
    'OpnPric' : 'open',
    'HghPric' : 'high',
    'LwPric' : 'low',
    'ClsPric' : 'close',
    'LastPric' : 'last',
    'PrvsClsgPric' : 'prev_close',
    'TtlTradgVol' : 'volume',
    'TtlTrfVal' : 'value',
    'TtlNbOfTxsExctd': 'trades',
    'TradDt' : 'date'
}

DATE_FORMATS = {1: '%d-%b-%Y', 2: '%d-%b-%Y', 3: '%Y-%m-%d'}

MAPS = {1: map_format1, 2: map_format2, 3: map_format3}