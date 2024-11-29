# Kraken Trading Bot

A Python-based trading bot designed to scalp **BTC/USDT** on Kraken. It uses **Relative Strength Index (RSI)** and **MACD** indicators to execute trades, aiming to increase USDT holdings. The bot is containerized using Docker for easy deployment and includes detailed logging.

---

## Features

- **Indicators Used**:
  - **RSI**: Identifies overbought/oversold conditions.
  - **MACD**: Tracks trend strength and crossovers.
- **Automated Trading**:
  - Executes buy orders when RSI indicates oversold and MACD signals a bullish crossover.
  - Executes sell orders when RSI indicates overbought and MACD signals a bearish crossover.
- **Secure Configuration**:
  - API credentials stored as environment variables.
  - Runs as a non-root user in the Docker container.
- **Comprehensive Logging**:
  - Logs trades, signals, and errors to both the console and a file for review.

---

## Project Structure

```plaintext
kraken_bot/
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # Dockerfile for containerizing the bot
├── requirements.txt           # Python dependencies
├── main.py                    # Main bot logic
├── config.py                  # Configuration file
├── utils/
│   ├── indicators.py          # RSI and MACD calculation utilities
│   └── logger.py              # Logging setup
└── logs/                      # Directory for log files
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
git clone https://github.com/your_username/kraken-trading-bot.git
cd kraken-trading-bot
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

## Configuration

You can customize the bot's behavior by modifying the config.py file. Below are the key configuration options:
RSI Settings

    RSI_PERIOD: The number of periods used to calculate the RSI. Default is 14.
    RSI_OVERBOUGHT: RSI value above which a sell signal is triggered. Default is 70.
    RSI_OVERSOLD: RSI value below which a buy signal is triggered. Default is 30.

MACD Settings

    MACD_SHORT: The short window period for MACD calculation. Default is 12.
    MACD_LONG: The long window period for MACD calculation. Default is 26.
    MACD_SIGNAL: The signal line window period for MACD calculation. Default is 9.

Trading Parameters

    TRADE_AMOUNT: The USDT amount to trade per transaction. Adjust according to your risk tolerance and account size. Default is 100.

Log Configuration

    LOG_FILE: The file path where logs will be saved. Default is logs/trading_bot.log.

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

