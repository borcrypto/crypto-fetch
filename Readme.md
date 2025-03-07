# BTC Price  Data Fetcher

This script retrieves historical BTC prices from Binance for the last specified number of weeks, formatted weekly, and saves the data directly to a Google Spreadsheet.

## Features
- Fetches weekly BTC/USDT closing prices for the past specified weeks.
- Formats the data with Year, Month, Week, and Price.
- Uploads the data automatically to Google Sheets.
- Displays progress in the terminal with colorized output.

## Prerequisites
- Python 3.10 or higher
- A Google Cloud project with Google Sheets API enabled
- A `credentials.json` file for Google API authentication

## Installation

### 1. Clone the repository
```sh
git clone https://github.com/borcrypto/crypto-price-fetch.git
cd crypto-price-fetch
```

### 2. Create a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Add Google API Credentials
Place your `credentials.json` file in the project root.

### 5. Configure `config.json`
Create a `config.json` file in the project root with the following structure:
```json
{
  "weeks": 4, //replace 
  "sheet_id": "1GaV0-6M1xQLBse8VjkG4B9Hjf-q6IMvRuhvTC2fDoO4",
  "symbol": "BTCUSDT"
}
```
- `weeks`: Number of weeks to fetch historical data for.
- `sheet_id`: Your Google Spreadsheet ID.
- `symbol`: The trading pair symbol (e.g., BTCUSDT, ETHUSDT, BNBUSDT).

## Usage
```sh
python main.py
```
This will fetch BTC prices and update your Google Sheet.

## Configuration
Modify `config.json` to change settings dynamically.

## Notes
- Ensure your Google Service Account has edit access to the spreadsheet.
- Avoid API rate limits by not running the script too frequently.

## License
MIT License

