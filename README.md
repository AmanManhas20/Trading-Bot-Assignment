# Binance Futures Testnet Trading Bot

This project is a small Python CLI app for placing `MARKET` and `LIMIT` orders on the Binance Futures Testnet (USDT-M). It is structured with separate client, validation, order, and CLI layers, and it logs API requests, responses, and errors to a file.

## Features

- Place `MARKET` and `LIMIT` orders on Binance Futures Testnet
- Supports both `BUY` and `SELL`
- Validates CLI input before hitting the API
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
  cli.py
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

3. Create environment variables for your Binance Futures Testnet credentials:

```bash
set BINANCE_API_KEY=your_testnet_key
set BINANCE_API_SECRET=your_testnet_secret
```

Optional:

```bash
set BINANCE_BASE_URL=https://testnet.binancefuture.com
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

