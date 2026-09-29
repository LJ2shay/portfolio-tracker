# Stock Portfolio Tracker

A full-stack web application built with Python and Flask that allows users to track their stock portfolio and watchlist in real time using live market data from Yahoo Finance.

---

## Features

- **Portfolio tracking** — Add and remove stock holdings with purchase price and date
- **Real-time prices** — Live stock prices fetched from Yahoo Finance API
- **Gain/Loss calculation** — Automatically calculates profit/loss per holding and total portfolio performance
- **Price history chart** — Interactive 6-month price chart for any stock
- **Watchlist** — Track stocks you're interested in without adding them to your portfolio
- **Stock detail page** — View company info, sector, 52-week high/low, and price history for any ticker
- **Input validation** — Handles invalid tickers, empty fields, and bad dates gracefully
- **Server-side caching** — Reduces redundant API calls by caching prices for 5 minutes

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Charting | Chart.js |
| Market Data | yfinance (Yahoo Finance API) |

---

## 📁 Project Structure
