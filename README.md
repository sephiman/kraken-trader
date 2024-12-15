# Kraken Trading Bot

A Python-based trading bot designed to scalp **BTC/USD** on Kraken. It uses **Relative Strength Index (RSI)** and **MACD** indicators to execute trades, aiming to increase USD holdings. The bot is containerized using Docker for easy deployment and includes detailed logging.

---

## Features

- **Automated Trading**:
  - Executes buy orders when RSI indicates oversold and MACD signals a bullish crossover.
  - Only adds more buy orders if the new price improves upon the last buy price (configurable threshold).
  - Executes sell orders when RSI indicates overbought and MACD signals a bearish crossover.

- **Technical Indicators**:
  - **RSI**: Identifies overbought/oversold conditions.
  - **MACD**: Measures trend momentum and identifies crossovers.
  - **Bollinger Bands**: Dynamic support/resistance for more accurate signals.

- **Trend & Timeframe Confirmation**:
  - **Trend Filter (Optional)**: Uses a moving average to confirm trend direction.  
    For example:
    - Only take buy signals if current price > MA (indicating an uptrend).
    - Only take sell signals if current price < MA (indicating a downtrend).
  - **Higher Timeframe Confirmation (Optional)**:  
    Confirms signals from the primary chart with a higher timeframe (e.g., 5m) RSI and MACD.  
    This helps reduce false signals by ensuring short-term setups align with broader market trends.

- **Daily Statistics Summary**:
  - At the end of each day (UTC), the bot automatically calculates and sends a Telegram message summarizing:
    - Current account balances
    - Profit/Loss for the last 24 hours
    - Profit/Loss for the last 7 days
    - Profit/Loss for the last 30 days
  - This daily report helps you track performance over multiple timeframes without manual effort.

- **Secure and Flexible**:
  - API credentials stored as environment variables for security.
  - Fully configurable trading parameters (e.g., trade amount, indicator thresholds, trend filters, higher timeframe confirmations).

- **Containerized Deployment**:
  - Easy to deploy with Docker and Docker Compose.

- **Detailed Logging**:
  - Logs buy/sell signals, trend conditions, higher timeframe confirmations, and indicator values.
  - Telegram alerts keep you informed of executed trades and daily performance metrics.

---

## Project Structure

```plaintext
kraken_bot/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Dockerfile for containerizing the bot
├── requirements.txt            # Python dependencies
├── main.py                     # Main entry point for the bot
├── config/                     # Configuration files and environment setup
│   └── config.py               # Configuration settings
├── core/                       # Core trading logic
│   ├── bot.py                  # Scalping bot logic
│   ├── account.py              # Account balance and trade execution
│   ├── indicators.py           # RSI, MACD, Bollinger Bands calculations
│   └── utils.py                # Utility functions (e.g., fetch price, OHLC data)
├── logs/                       # Directory for log files
│   └── trading_bot.log         # Default log file
├── utils/                      # Logging and helper utilities
│   ├── logger.py               # Logger setup
│   └── exceptions.py           # Custom exception handling
└── tests/                      # Unit tests for components
    └── test_indicators.py      # Example test for indicator calculations
```

## Prerequisites

- **Docker**:
  - Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
- **Kraken API Credentials**:
  - Create API keys from the [Kraken Dashboard](https://www.kraken.com/).
  - Ensure your API key has permission to execute trades.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sephiman/kraken-trader.git
cd kraken-trader
```

### 2. Set Up Environment Variables

Replace the variables in the docker-compose.yml with your Kraken API keys:

    KRAKEN_API_KEY=your_api_key
    KRAKEN_API_SECRET=your_api_secret

### 3. Build and Run the Bot

Use Docker Compose to build and start the bot:
```bash
docker-compose up --build
```


---

## Configuration

The bot's behavior can be customized by modifying `config.py`:

### RSI Settings
- `RSI_PERIOD`: Number of periods for RSI calculation.
- `RSI_OVERBOUGHT`: Sell signal threshold.
- `RSI_OVERSOLD`: Buy signal threshold.

### MACD Settings
- `MACD_SHORT`, `MACD_LONG`, `MACD_SIGNAL`: Short, long, and signal periods for MACD.

### Bollinger Bands
- `BOLLINGER_PERIOD`, `BOLLINGER_STD_DEV`: Period and standard deviation for Bollinger Bands.

### Trend Filter (Optional)
- `TREND_FILTER_ENABLED`: Set to `True` to enable trend filtering.
- `TREND_MA_PERIOD`: Moving average period used to determine overall trend direction.

### Higher Timeframe Confirmation (Optional)
- `HIGHER_TF_CONFIRMATION_ENABLED`: Set to `True` to enable higher timeframe checks.
- `HIGHER_TF_INTERVAL`: Interval (in minutes) for the higher timeframe data.
- `HIGHER_TF_RSI_PERIOD`, `HIGHER_TF_RSI_OVERBOUGHT`, `HIGHER_TF_RSI_OVERSOLD`: RSI parameters for higher timeframe analysis.
- `HIGHER_TF_MACD_SHORT`, `HIGHER_TF_MACD_LONG`, `HIGHER_TF_MACD_SIGNAL`: MACD parameters for the higher timeframe.

### Trading Parameters
- `TRADE_AMOUNT`: USD amount to trade per transaction.
- `NEW_BUY_THRESHOLD`: Threshold for adding new buy orders at improved prices.

### Logs
- `LOG_FILE`: Path to log file.

## Telegram Integration

The bot can send real-time trade notifications and daily performance summaries to your Telegram chat:

- **Trade Alerts**: Notifies you of executed buy and sell orders, as well as failures.
- **Daily Summary**: Sends a daily report including balances and profit/loss over multiple timeframes.

Configure your Telegram bot token and chat ID in `docker-compose.yml` or through environment variables.

## Logs

    The bot maintains comprehensive logs that include buy/sell signals, trade execution details, and errors.

    Logs are stored in the logs/ directory.

    Example log snippet:

    2024-11-29 12:00:00 - INFO - Starting Kraken Trading Bot
    2024-11-29 12:01:00 - INFO - Buy Signal Detected
    2024-11-29 12:01:01 - INFO - Buy order placed: { ...order details... }
    2024-11-29 12:02:00 - INFO - Sell Signal Detected
    2024-11-29 12:02:01 - INFO - Sell order placed: { ...order details... }

    Logs are essential for debugging and tracking the bot's performance.

## Disclaimer

This bot is provided as is and for educational purposes only. Trading cryptocurrencies involves significant financial risk. There is no guarantee of profitability, and you may lose some or all of your investment. Use this bot at your own risk and consider consulting a financial advisor.

## Contributing

Contributions are welcome! If you would like to improve the bot or report a bug, please:

    Fork the repository.
    Create a new branch for your changes.
    Submit a pull request with a clear description of your improvements or fixes.

