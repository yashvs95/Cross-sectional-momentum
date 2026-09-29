import pandas as pd


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


def detect_format(cols):
    """detect_format takes column names as input and detects the format. Flags if missing columns or wrong sort of data here"""
    cols = set(cols)
    if 'TckrSymb' in cols:
        fmt = 3
    elif 'SYMBOL' in cols and 'ISIN' in cols:
        fmt = 2
    elif 'SYMBOL' in cols:
        fmt = 1
    else:
        raise ValueError(f'Unknown format: {sorted(cols)}')

    missing = set(MAPS[fmt]) - cols
    if missing:
        raise ValueError(f'File with format {fmt} is missing : {sorted(missing)}')
    return fmt

def standardize(path):
    """Takes as input a path to a bhavcopy record, then puts it in a standard format and deals with missing values"""
    # Strange pitfall here that NA is a series code used by NSE so we need to change what pandas views as a missing value
    df = pd.read_csv(path, index_col = False, keep_default_na=False, na_values = [''])
    fmt = detect_format(df.columns)

    #Older bhavcopies have unnamed extra columns, checking them and dropping them
    unnamed = [col for col in df.columns if col.startswith('Unnamed')]
    for col in unnamed:
        if df[col].notna().any():
            raise ValueError(f'{path}: column {col} is not empty')
    df = df.drop(columns = unnamed)

    df = df.rename(columns = MAPS[fmt])
    df['fmt'] = fmt

    #take care of missing data
    for col in STANDARD_COLS:
        if col not in df.columns:
            df[col] = pd.NA
    #Some clean up of data and formatting
    df['date'] = pd.to_datetime(df['date'], format = DATE_FORMATS[fmt])

    for col in ['symbol', 'series', 'isin']:
        df[col] = df[col].astype('string').str.strip()
    for col in ['open', 'high', 'low', 'close', 'last', 'prev_close', 'volume', 'value', 'trades']:
        df[col] = pd.to_numeric(df[col])

    return df[STANDARD_COLS]


def validate(df, tolerance = 0.005, e =0.006):
    """ Checks a bhavcopy record for structural issues and bugs. A standardized copy of bhavcopy is to be passed here."""
    # Strict checks
    if df['date'].nunique() != 1:
        raise ValueError(f'There are multiple ({df["date"].nunique()}) dates in this bhavcopy record')
    duplicates = df.duplicated(subset = ['symbol', 'series', 'date'])
    if duplicates.any():
        raise ValueError('There are duplicate stock values in here')
    if df[['date','symbol','series', 'close']].isna().any().any():
        raise ValueError('Missing critical values for momentum calculation')

    #Looser checks
    #Upon inspection closing prices sometimes jiggled out of the low high range due to afterhours trading calculations that NSE does. added an epsilon (the number e in the function definition) to deal with this
    bad = (
            ~((df['low']*(1-e) <= df['close']) & (df['close'] <= df['high']*(1+e)))
            |~((df['low'] <= df['open']) & (df['open'] <= df['high']))
            |(df[['open', 'high', 'low', 'close']] <= 0).any(axis=1)
            |(df[['volume', 'value']] < 0).any(axis=1)
    )
    error_rate = bad.mean()
    if error_rate >= tolerance:
        raise ValueError(f'{error_rate} of data points are bad surpassing our tolerance of {tolerance}')
    return df[bad]