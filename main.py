import requests
import datetime
import time
import json
import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored

# Baca config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

def get_historical_prices(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    prices = []
    week_count = 1
    
    while start_time < end_time:
        print(colored(f"Getting data for week {week_count}...", "cyan"))
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": int(start_time.timestamp() * 1000),
            "limit": 1  # Ambil satu data per permintaan
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data:
            timestamp = datetime.datetime.fromtimestamp(data[0][0] / 1000, datetime.timezone.utc)
            prices.append({
                "time": timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                "year": timestamp.strftime('%Y'),
                "month": timestamp.strftime('%m'),
                "week": timestamp.strftime('%W'),
                "price": f"USD {float(data[0][4]):,.2f}"  # Format harga dengan USD
            })
        
        start_time += datetime.timedelta(weeks=1)  # Loncat per minggu
        week_count += 1
        time.sleep(0.5)  # Hindari rate limit
    
    # Urutkan data dari terbaru ke terlama
    prices.sort(key=lambda x: x["time"], reverse=True)
    
    return prices

def save_to_spreadsheet(prices, sheet_id):
    # Autentikasi dengan Google Sheets API
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://www.googleapis.com/auth/spreadsheets"])
    client = gspread.authorize(creds)
    
    # Buka spreadsheet menggunakan ID
    spreadsheet = client.open_by_key(sheet_id)
    sheet = spreadsheet.sheet1
    
    # Hapus data lama
    sheet.clear()
    
    # Tulis header
    headers = ["Date", "Year", "Month", "Week", "Price"]
    sheet.append_row(headers)
    
    # Format header menjadi bold
    header_range = sheet.range(1, 1, 1, len(headers))  # Ambil range header (baris 1)
    for cell in header_range:
        cell.text_format = {"bold": True}  # Set teks menjadi bold
    sheet.update_cells(header_range)  # Update format ke Google Sheets
    
    # Tulis data
    for entry in prices:
        sheet.append_row([entry['time'], entry['year'], entry['month'], entry['week'], entry['price']])
    
    print(colored("Data has been updated in Google Sheets", "green"))

if __name__ == "__main__":
    # Ambil nilai dari config.json
    symbol = config["symbol"]
    sheet_id = config["sheet_id"]
    weeks = config["weeks"]
    
    interval = "1w"  # 1 minggu
    end_time = datetime.datetime.now(datetime.timezone.utc)
    start_time = end_time - datetime.timedelta(weeks=weeks)  # Sesuaikan dengan nilai weeks dari config.json
    
    prices = get_historical_prices(symbol, interval, start_time, end_time)
    save_to_spreadsheet(prices, sheet_id)