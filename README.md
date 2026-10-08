# Telegram Cryptocurrency & Market Bot

A Telegram bot for checking cryptocurrency, forex, commodities, and USD prices directly from Telegram.

## Features

- Cryptocurrency price lookup
- Forex price lookup
- Commodity price lookup
- USD/USDT to Toman price
- Cryptocurrency search
- Price change information
- Price charts
- Multiple chart timeframes
- Required channel membership
- Admin panel
- MySQL database

## Charts

The bot can generate price charts for supported markets.

Available timeframes:

- 5 minutes
- 15 minutes
- 30 minutes
- 60 minutes

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/parsa-ag2/Tel-Bot-Cryptocurrency.git
cd Tel-Bot-Cryptocurrency
```

### 2. Install requirements

Install the required Python packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Create the `.env` file

Create a `.env` file in the root directory of the project yourself.

Example:

```env
BOT_TOKEN=your_telegram_bot_token
TWELVE_DATA_API_KEY=your_twelve_data_api_key

DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password

OWNER_ID=your_telegram_id
```

Replace the values with your own credentials and configuration.

### 4. Set up MySQL

Create a MySQL database for the bot.

Example:

```sql
CREATE DATABASE telegram_bot;
```

Then configure the database credentials in your `.env` file.

### 5. Run the bot

```bash
python main.py
```

## How It Works

The bot receives the user's message in Telegram and identifies what market or asset the user is asking about.

It supports Persian and English names and aliases for supported markets. The bot retrieves market data from external APIs, processes the response, and sends the current price and related information back to the user.

Price data is cached for a short period to reduce unnecessary API requests.

## Example Usage

In a Telegram group, you can write:

```text
دلار
```

The bot returns the current USD/USDT price in Toman.

You can also write:

```text
بیتکوین
```

The bot returns the current Bitcoin price and its price change.

Example response:

```text
Bitcoin
Price: $XX,XXX
24h Change: X.XX%
```

You can also search for other supported cryptocurrencies, forex pairs, and commodities using their names or supported aliases.

## Required Channel

The bot can require users to join specific Telegram channels before using its features.

## Admin Panel

Administrators can manage bot settings and required channels through the administration functionality.

## Environment Variables

Sensitive information such as API keys, Telegram bot tokens, database credentials, and owner IDs should be stored in `.env`.

Do not commit your `.env` file to GitHub.

## Database

The project uses MySQL to store bot-related data such as:

- Administrators
- Required channels
- Bot settings

## Usage Note

Use Persian or English asset names in Telegram to request supported market prices.

## License

This project is provided for educational and development purposes.
