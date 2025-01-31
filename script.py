import yfinance as yf
import pandas as pd
import datetime

from save_data import save_market_report

# Creates empty dataframe to add data too
all_data = pd.DataFrame(columns=["Ticker", "Asset Name", "Open", "Close"])

def get_next_trading_day(date):
    """Moves forward to the next available trading day if the given date is a holiday or weekend."""
    while True:
        stock_data = yf.download("SPY", start=date, end=date + datetime.timedelta(days=1))
        if not stock_data.empty:
            return date
        date += datetime.timedelta(days=1)  # Move forward if data is missing

# Finds the last friday and the monday before so that I can use the dates to find last weeks performance
def get_monday_and_friday():
    today = datetime.date.today() # Gets todays date

    # Gets last Friday
    days_to_last_friday = (today.weekday() - 4) + 7  # Finds how many days I am from the next friday, since Friday is day 04, then adds 7 to see how many days I am away from last friday
    last_friday = today - datetime.timedelta(days=days_to_last_friday) # finds last friday by subrtacing the todays date and the amount of days I am from last friday

    # Calculate the Monday before last Friday
    monday_before = last_friday - datetime.timedelta(days=4) # finds the monday since it is 4 days before friday

    monday_before = get_next_trading_day(monday_before)
    last_friday = get_next_trading_day(last_friday)

    return monday_before, last_friday

def get_stock_prices(stock_symbol):
    monday, friday = get_monday_and_friday()

    # Gets stock data from yahoo finance API
    stock_data = yf.download(stock_symbol, start=monday, end=friday + datetime.timedelta(days=1)) # need to add one day to end date so that it includes the friday since the api is exclusive

    # indexes the data and filters for monday and friday
    monday_data = stock_data.loc[str(monday)]
    friday_data = stock_data.loc[str(friday)]

    try:
        asset_name = yf.Ticker(stock_symbol).info['longName']
    except Exception as e:
        print(f"Error fetching asset name for {stock_symbol}: {e}")
        asset_name = stock_symbol

    return {
        'asset_name': asset_name,
        "week_open": monday_data['Open'],
        "week_close": friday_data['Close'],
    } # returns the open and close prices for the week

def add_to_df(stock_symbol):
    try:
        stock_data = get_stock_prices(stock_symbol)

        stock_df = pd.DataFrame({'Asset Name': stock_data['asset_name'], 'Open': stock_data['week_open'], 'Close': stock_data['week_close']}).reset_index() # creates a new df for the inputed stock, index is reset so that 'ticker' is on the same level as 'open' and 'close' column

        global all_data #
        all_data = pd.concat([all_data, stock_df], ignore_index=True) # concats the new df, stock_df, to the all_data df

    except Exception as e:
        print(f"Error: {stock_symbol}: {e}") # if there is an error, ignore it


    return all_data

tickers = ["^GSPC", "^DJI", "^IXIC", "^FTSE", "^FCHI", "INTC", "LMT", "MSFT",
           "AMZN", "TSLA", "GOOG", "META", "AXON", "PLTR", "NVDA", "000001.SS",
           "^NSEI", "^HSI", "^GSPTSE", '^TWII',"GC=F", "SI=F", "BZ=F", "ZW=F",
           "HG=F", "EURUSD=X", "USDJPY=X", "GBPUSD=X", "USDCNY=X", "USDCHF=X",
           "BTC-USD", "ETH-USD", "BNB-USD", "XRP-USD", "ADA-USD"] # all the tickers i need for the newsletter

for stock in tickers: # runs the function add_to_df for each ticker that i need
    add_to_df(stock)

# calculates the rest of the data i need for the newsletters
all_data['Absolute Change'] = all_data['Close'] - all_data['Open'] # calculates the absolute change
all_data['Percentage Change'] = ((all_data['Close'] - all_data['Open']) / all_data['Open']) * 100 # calculates the percentage change

# Rounding the data to 2 decimal places
all_data['Open'] = all_data['Open'].round(2)
all_data['Close'] = all_data['Close'].round(2)
all_data['Absolute Change'] = all_data['Absolute Change'].round(2)

# convert to a %
all_data['Percentage Change'] = all_data['Percentage Change'].round(2).astype(str) + '%'

print(all_data)

# This uses the save_data to push to a HTML file
monday, friday = get_monday_and_friday()
save_market_report(all_data, monday, friday)
