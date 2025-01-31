# Investment club newsletter financial data

## Purpose
I am part of the **investment club** newsletter and every week we use information about certain stocks in our newsletter. I found it annoying to always find the data, calculate it, then input it, so I decided to create this script using yahoo finance api to automate this process. For certain stocks, it calculates the opening and closing price of last week, the abolsute change, and the relative change.

**This information is updated weekly, at 00:30AM GMT+1, it can be [here](https://ntello23.github.io/session_3_homework/market_report.html)**

## How to use
To use this file, run the code,
```
pip install -r requirements.txt
```
in the terminal to download the libraries and versions that I used. Then run the file _'script.py'_. A pandas dataframe will be printed in the console with infomration for each stock/asset. To use your own tickers, replace the elements in the list in line 51 called _tickers_ with the tickers you want.
