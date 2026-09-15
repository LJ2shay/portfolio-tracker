import sqlite3 

def init_db():
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("""                              
        CREATE TABLE IF NOT EXISTS holdings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker      TEXT NOT NULL,
            shares      REAL NOT NULL,
            buy_price   REAL NOT NULL,
            buy_date    TEXT NOT NULL
        )   
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker  TEXT NOT NULL UNIQUE                         
        )
    """)

    conn.commit()
    conn.close()

def add_holding(ticker, shares, buy_price, buy_date):
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("""
        INSERT INTO holdings (ticker, shares, buy_price, buy_date)
        VALUES (?, ?, ?, ?)
    """, (ticker, shares, buy_price, buy_date))

    conn.commit()
    conn.close()

def get_all_holdings():
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("SELECT * FROM holdings")
    rows = cursor.fetchall()
    conn.close()

    return rows

def delete_holding(holding_id):
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("""
        DELETE FROM holdings
        WHERE id = ?
    """, (holding_id,))

    conn.commit()
    conn.close()

def add_to_watchlist(ticker):
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("""
        INSERT OR IGNORE INTO watchlist (ticker)
        VALUES (?)
    """, (ticker,))

    conn.commit()
    conn.close()

def get_watchlist():
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("SELECT * FROM watchlist")
    rows = cursor.fetchall()
    conn.close()

    return rows

def remove_from_watchlist(ticker):
    conn = sqlite3.connect("portfolio.db")          # connection to file
    cursor = conn.cursor()                          # cursor object to execute sql

    cursor.execute("""
        DELETE FROM watchlist
        WHERE ticker = ?
    """, (ticker,))

    conn.commit()
    conn.close()
