# Kraken Trading Bot

A Python-based trading bot designed to scalp **BTC/USD** on Kraken. It uses **Relative Strength Index (RSI)** and **MACD** indicators to execute trades, aiming to increase USD holdings. The bot is containerized using Docker for easy deployment and includes detailed logging.

---

## Features

- **Automated Trading**:
  - Executes buy orders when RSI indicates oversold and MACD signals a bullish crossover.
  - Executes sell orders when RSI indicates overbought and MACD signals a bearish crossover.
- **Technical Indicators**:
  - **RSI**: Identifies overbought/oversold market conditions.
  - **MACD**: Measures trend momentum and identifies crossovers.
  - **Bollinger Bands**: Adds dynamic support/resistance for more accurate signals.
- **Secure and Flexible**:
  - API credentials stored as environment variables for security.
  - Fully configurable trading parameters (e.g., trade amount, indicator thresholds).
- **Containerized Deployment**:
  - Easy to deploy with Docker and Docker Compose.
- **Detailed Logging**:
  - Logs buy/sell signals, trade execution details, and errors to both the console and a file for review.

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

### **6. Configuration**
Current Text:
> Lists configurable parameters from `config.py`.

**Suggested Changes**:
- Include detailed examples for how configuration changes impact the bot.
- Mention the importance of setting trade parameters based on risk tolerance.

**Revised Text**:
```markdown
## Configuration

The bot's behavior can be customized by modifying `config.py`:

### RSI Settings
- `RSI_PERIOD`: Number of periods for RSI calculation. Default is 14.
- `RSI_OVERBOUGHT`: Sell signal threshold. Default is 60.
- `RSI_OVERSOLD`: Buy signal threshold. Default is 40.

### MACD Settings
- `MACD_SHORT`: Short window for MACD. Default is 12.
- `MACD_LONG`: Long window for MACD. Default is 26.
- `MACD_SIGNAL`: Signal line period. Default is 9.

### Trading Parameters
- `TRADE_AMOUNT`: USD amount to trade per transaction. Default is 10.

### Logs
- `LOG_FILE`: Path to log file. Default is `logs/trading_bot.log`.

> **Tip**: Start with small trade amounts and backtest configurations before running live.


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

