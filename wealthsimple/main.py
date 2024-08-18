import os
import sys
import pandas as pd
from datetime import datetime

def process_csv(file_path):
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        return None

    df = df[df['transaction'].isin(['BUY', 'SELL'])]
    
    if df.empty:
        return None

    result = []
    for _, row in df.iterrows():
        description_parts = row['description'].split(':')
        symbol = description_parts[0].split('-')[0].strip()
        action_parts = description_parts[1].split()
        quantity = float(action_parts[1])
        
        if row['transaction'] == 'SELL':
            quantity = -quantity

        date = datetime.strptime(row['date'], '%Y-%m-%d').strftime('%Y-%m-%d')
        price = abs(float(row['amount']) / quantity)

        result.append({
            'Symbol': symbol,
            'Date': date,
            'Quantity': quantity,
            'Price': price,
            'Currency': 'CAD'
        })

    return pd.DataFrame(result)

def main(folder_name):
    all_data = []
    for file in os.listdir(folder_name):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_name, file)
            df = process_csv(file_path)
            if df is not None:
                all_data.append(df)

    if not all_data:
        print("No valid data found in the CSV files.")
        return

    result_df = pd.concat(all_data, ignore_index=True)
    result_df = result_df[['Symbol', 'Date', 'Quantity', 'Price', 'Currency']]
    
    output_file = f'wealthsimple_{folder_name}.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Aggregated data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py folder_name")
    else:
        main(sys.argv[1])
