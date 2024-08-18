import sys
import os
import re
import PyPDF2
import pandas as pd
from datetime import datetime

def extract_trades_from_pdf(pdf_path):
    trades = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Extract quantity and price
    quantity_price_match = re.findall(r'\b\d+(?:\.\d+)?\s\d+(?:\.\d+)?\b', text)
    if quantity_price_match:
        quantity, price = quantity_price_match[-1].split(" ")
    else:
        print(f"Could not extract quantity and price from {pdf_path}")
        return pd.DataFrame()

    # Extract symbol
    symbol_match = re.split(r'Ticker symbol: ', text)
    if len(symbol_match) > 1:
        symbol = symbol_match[1].split('\n')[0].strip()
    else:
        print(f"Could not extract symbol from {pdf_path}")
        return pd.DataFrame()

    # Extract date
    date_match = re.split(r'Transaction on ', text)
    if len(date_match) > 1:
        date_str = date_match[1].split('\n')[0].strip()
        date = datetime.strptime(date_str, "%B %d, %Y").strftime('%Y-%m-%d')
    else:
        print(f"Could not extract date from {pdf_path}")
        return pd.DataFrame()

    # Determine currency
    currency = 'USD' if re.findall(r'USD', text) else 'CAD'
    if currency == 'CAD':
        symbol = f'{symbol}.TO'

    trades.append({
        'Symbol': symbol,
        'Date': date,
        'Quantity': float(quantity),
        'Price': float(price.replace(',', '')),
        'Currency': currency
    })

    return pd.DataFrame(trades)

def main(folder_path):
    all_trades = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            trades_df = extract_trades_from_pdf(pdf_path)
            if not trades_df.empty:
                all_trades.append(trades_df)

    if not all_trades:
        print("No trade data found in the PDF files.")
        return

    result_df = pd.concat(all_trades, ignore_index=True)
    output_file = f'td_{folder_path}.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Aggregated trade data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py folder_path")
    else:
        main(sys.argv[1])