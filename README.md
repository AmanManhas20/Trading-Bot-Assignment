# Binance Futures Testnet Trading Bot

This project is a small Python trading bot for placing `MARKET` and `LIMIT` orders on the Binance Futures Testnet (USDT-M). It includes both a command-line interface and a lightweight animated web dashboard, with separate client, validation, order, and logging layers.

## Features

- Place `MARKET` and `LIMIT` orders on Binance Futures Testnet
- Supports both `BUY` and `SELL`
- Validates CLI input before hitting the API
- Includes a clean minimal web UI with smooth animations
- Logs requests, responses, and failures to `logs/trading_bot.log`
- Keeps API access isolated in a reusable client layer

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    logging_config.py
    orders.py
    validators.py
  web/
    index.html
    styles.css
    app.js
  cli.py
  webapp.py
README.md
requirements.txt
.env.example
```

## Setup

1. Create and activate a Python 3 virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` into your shell environment and set your Binance Futures Testnet credentials:

```bash
set BINANCE_API_KEY=your_testnet_key
set BINANCE_API_SECRET=your_testnet_secret
```

Optional:

```bash
set BINANCE_BASE_URL=https://testnet.binancefuture.com
```

4. Verify the local project setup:

```bash
python -m unittest discover -s tests
python -m trading_bot.cli --help
python -c "from trading_bot.webapp import run_server; print('web import ok')"
```

## Usage

### Market order

```bash
python -m trading_bot.cli --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

### Limit order

```bash
python -m trading_bot.cli --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 80000
```

## Web UI

Start the dashboard server:

```bash
python -m trading_bot.webapp
```

Then open:

```text
http://127.0.0.1:8000
```

The UI submits orders through the same Python validation and Binance client logic used by the CLI.

## Output

The CLI prints:

- order request summary
- order response details
- success or failure message
- log file location

## Logging

Logs are written to:

```text
logs/trading_bot.log
```

The log file captures:

- submitted order payloads
- Binance API responses
- validation errors
- API/network failures

## Assumptions

- Only USDT-M futures pairs are in scope for this assignment
- `LIMIT` orders use `GTC`
- API credentials are provided through environment variables instead of hardcoding secrets
- The assignment is evaluated against Binance Futures Testnet, not mainnet

## Submission Notes

To fully satisfy the deliverables, run:

- one successful `MARKET` order
- one successful `LIMIT` order

Then include the generated `logs/trading_bot.log` file or split copies of those runs in your final submission.

## Local Development Notes

- `__pycache__` files, local `.env` files, and generated logs are ignored via `.gitignore`
- The project uses only the Python standard library
- Tests cover validation and payload formatting logic; live order placement still requires valid Binance Testnet credentials

