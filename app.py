from flask import Flask, render_template, request, redirect, url_for, jsonify
from database import init_db, add_holding, get_all_holdings, delete_holding, get_watchlist, add_to_watchlist, remove_from_watchlist
from stock_api import get_stock_price, get_price_history, get_stock_info
from datetime import date

import time

app = Flask(__name__)

init_db()

price_cache = {}
CACHE_TTL = 300

def get_cached_price(ticker):
    now = time.time()

    if ticker in price_cache:
        price, ts = price_cache[ticker]

        if now - ts < CACHE_TTL:
            return price
        
    price = get_stock_price(ticker)
    price_cache[ticker] = (price, time.time())
    return price

def render_portfolio(error=None):
    holdings = get_all_holdings()
    enriched = []
    for h in holdings:
        id, ticker_h, shares_h, buy_price_h, buy_date_h = h
        current_price = get_cached_price(ticker_h)
        gain_loss = round((current_price - buy_price_h) * shares_h, 2)
        gain_pct = round(((current_price - buy_price_h) / buy_price_h) * 100, 2) if buy_price_h else 0
        total_value = round(current_price * shares_h, 2)
        enriched.append({
            "id": id,
            "ticker": ticker_h,
            "shares": shares_h,
            "buy_price": buy_price_h,
            "buy_date": buy_date_h,
            "current_price": current_price,
            "gain_loss": gain_loss,
            "gain_pct": gain_pct,
            "total_value": total_value
        })
    total_value = sum(h["total_value"] for h in enriched)
    total_gain = sum(h["gain_loss"] for h in enriched)

    return render_template("portfolio.html",
                           holdings=enriched,
                           total_value=total_value,
                           total_gain=total_gain,
                           error=error)

def render_watchlist(error=None):
    watchlist = get_watchlist()
    enriched = []

    for item in watchlist:
        id, ticker = item

        current_price = get_cached_price(ticker)

        enriched.append({
            "id": id,
            "ticker": ticker,
            "current_price": current_price
        })
    return render_template("watchlist.html", watchlist=enriched, error=error)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/portfolio")
def portfolio():
    return render_portfolio()

@app.route("/watchlist")
def watchlist():
    return render_watchlist()

@app.route("/add", methods=["POST"])
def add():
    # Get values from form
    ticker = request.form["ticker"]
    shares = request.form["shares"]
    buy_price = request.form["buy_price"]
    buy_date = request.form["buy_date"]
    error = None

    # Checks if anything is empty
    if not ticker:
        error = "Ticker cannot be empty"
    elif not shares:
        error = "Shares cannot be empty"
    elif not buy_price:
        error = "Buy price cannot be empty"
    elif not buy_date:
        error = "Buy date cannot be empty"
    else: 
        try:
            # Converts non empty shares/buy_price number to float
            shares = float(shares)
            buy_price = float(buy_price)

            # Error checks to make sure numbers are greater than or equal to zero
            if shares <= 0:
                error = "Shares must be greater than 0"
            elif buy_price <= 0: 
                error = "Buy price must be greater than 0"
            else:
                # Check if ticker is valid by trying to fetch its price
                test_price = get_stock_price(ticker)
                if test_price == 0.0:
                    error = f"'{ticker}' is not a valid ticker symbol."
                else:
                    # Date check
                    today = date.today()
                    buy_date_obj = date.fromisoformat(buy_date)
                    if buy_date_obj >= today:
                        error = "Buy date must be in the past."
                    else:
                        # No errors so updates page
                        ticker = ticker.upper()
                        add_holding(ticker, shares, buy_price, buy_date)
                        return redirect(url_for("portfolio"))
        except ValueError:
            error = "Shares and buy price must be valid numbers."

    # If it reaches here something went wrong — reloads portfolio with error
    return render_portfolio(error)
    
        

@app.route("/delete/<int:holding_id>")
def delete(holding_id):
    delete_holding(holding_id)

    return redirect(url_for("portfolio"))

@app.route("/watchlist/add", methods=["POST"])
def watchlist_add():
    # Gets ticker from form
    ticker = request.form["ticker"]
    error = None

    # Temp price to check if ticker is valid
    temp_price = get_cached_price(ticker)

    # If temp_price is zero, ticker does not exist
    if temp_price == 0.0:
        error = f"'{ticker}' is not a valid ticker symbol."
    else:
        # No errors
        ticker = ticker.upper()
        add_to_watchlist(ticker)
        return redirect(url_for("watchlist"))
    
    # If it gets here theres an error - reloads watchlist with error
    return render_watchlist(error)

@app.route("/watchlist/remove/<ticker>")
def watchlist_remove(ticker):
    remove_from_watchlist(ticker)
    return redirect(url_for("watchlist"))

@app.route("/api/stock/<ticker>")
def info(ticker):
    data = get_stock_info(ticker)
    return jsonify(data)

@app.route("/api/history/<ticker>")
def history(ticker):
    data = get_price_history(ticker, "6mo")
    return jsonify(data)

@app.route("/stock/<ticker>")
def stock(ticker):
    return render_template("stock.html", ticker=ticker)

if __name__ == "__main__": 
    app.run(debug=True)
