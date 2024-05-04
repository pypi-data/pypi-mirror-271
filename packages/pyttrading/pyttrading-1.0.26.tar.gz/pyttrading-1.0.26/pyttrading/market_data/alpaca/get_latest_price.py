from dotenv import dotenv_values
from alpaca_trade_api.rest import REST, TimeFrame
from datetime import datetime, timedelta
import pytz
import pandas as pd 

config = dotenv_values(".env")

api_key = config.get('ALPACA_API_KEY')
api_secret = config.get('ALPACA_API_SECRET')
alpaca_api_url = "https://paper-api.alpaca.markets"

api = REST(api_key, api_secret, alpaca_api_url)

def _get_bars(start_time = None, symbol = "TNA", end_time = None, is_crypto = False, api = None):
    
    symbol = "TNA"
    is_crypto = False
    get_latest_date = False
    if not is_crypto:
        timezone = pytz.timezone("America/New_York")
        now = datetime.now(tz=timezone) 
        time_delta = now - end_time
        if time_delta < timedelta(minutes=15):
            get_latest_date = True
            end_time_adjusted = (end_time - timedelta(minutes=15)).replace(microsecond=0).isoformat()
        else:
            end_time_adjusted = (end_time - timedelta(minutes=1)).replace(microsecond=0).isoformat()

        bars = api.get_bars(symbol, TimeFrame.Minute, start_time.isoformat(), end_time_adjusted, adjustment='raw').df
        
        if get_latest_date:
            bars_latest = api.get_latest_bar(symbol)
            latest_bar_df = pd.DataFrame([{
                'close': bars_latest.close,
                'high': bars_latest.high,
                'low': bars_latest.low,
                'trade_count': bars_latest.trade_count,
                'open': bars_latest.open,
                'volume': bars_latest.volume,
                'vwap': bars_latest.vwap
            }], index=[pd.Timestamp(bars_latest.timestamp)])

            bars = pd.concat([bars, latest_bar_df])

    else:
        # Fetch cryptocurrency data using Alpaca's get_crypto_bars method
        end_time_adjusted = (end_time - timedelta(minutes=1)).replace(microsecond=0).isoformat()
        bars = api.get_crypto_bars(symbol, TimeFrame.Minute, start_time.isoformat(), end_time_adjusted).df


    return bars

def _adjust_time_window(start_time, symbol, end_time, is_crypto, api):
    # Check further in the past if the recent data is not accessible
    adjustment_minutes = [1000, 10000]  # Extending the window in steps
    for minutes in adjustment_minutes:
        start_time_adjusted = end_time - timedelta(minutes=minutes)
        bars = _get_bars(start_time_adjusted, symbol, end_time, is_crypto, api)
        if len(bars) > 0:
            return bars
    return None  # Return None if no bars were found

def get_assert_latest_price(symbol, date=None, is_crypto=True, api=None):

    timezone = pytz.timezone("America/New_York")
    
    if date is None:
        end_time = datetime.now(tz=timezone)
    else:
        end_time = timezone.localize(datetime.strptime(date, '%Y-%m-%d %H:%M:%S'))

    start_time = end_time - timedelta(minutes=300)
    bars = _get_bars(start_time, symbol, end_time, is_crypto, api=api)

    if len(bars) == 0: 
        bars = _adjust_time_window(start_time, symbol, end_time, is_crypto, api)

    if bars is not None and len(bars) > 0:
        price = bars.iloc[-1]
        return price
    return None  # Return None if no valid price data was found


def get_latest_quote_price(symbol, is_crypto=False, api=None):
    """
    Retrieves the latest quote price for a given symbol (equity or cryptocurrency).
    
    Args:
    - symbol (str): The symbol for which to get the quote.
    - is_crypto (bool): Flag to determine if the symbol is a cryptocurrency.
    - api (REST): The Alpaca Trade API client instance.
    
    Returns:
    - float: The latest quote price or None if not available.
    """
    if is_crypto:
        quote = api.get_latest_crypto_bars(symbol)
    else:
        quote = api.get_latest_crypto_trades(symbol)

    if quote:
        return quote['askprice'] if 'askprice' in quote else None
    return None