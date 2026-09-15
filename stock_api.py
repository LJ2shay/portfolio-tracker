import yfinance as yf

def get_stock_price(ticker):
    try:
        # Ticker object for given stock and gets today's price
        stock = yf.Ticker(ticker)                   
        data = stock.history(period='1d')           

        if data.empty:
            data = stock.history(period='5d')
        
        if data.empty:
            return 0.0
        
        # Gets last closing price and rounds it
        return round(data["Close"].iloc[-1], 2)     
    except Exception:
        return 0.0
    
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)

    # fetch a large dictionary of metadata about the stock                   
    info = stock.info 

    return {
        "name": info.get("longName", ticker),           # full company name, falls back to ticker if missing
        "price": get_stock_price(ticker),               # reuse function above to get price
        "sector": info.get("sector", "N/A"),            # industry sector
        "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),# highest price in last 52 weeks (year)
        "52w_low": info.get("fiftyTwoWeekLow", "N/A")   # lowest price in last 52 weeks (year)
    }

def get_price_history(ticker, period):
    stock = yf.Ticker(ticker)    
    # gets historical data for given period               
    history = stock.history(period=period)      

    dates = list(history.index.strftime("%Y-%m-%d"))    #convert the date index to list "YYYY-MM-DD"
    prices = list(history["Close"])                     # gets closing prices as list

    return {
        # list of dates : x axis for chart
        "dates": dates, 
        # list of prices : y axis for chart    
        "prices": prices    
    }