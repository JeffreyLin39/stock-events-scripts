import os
import sys
import pandas as pd

def process_ibkr_csv(file_path):
    try:
        df = pd.read_csv(file_path, skiprows=6)
    except pd.errors.EmptyDataError:
        return None

    stocks_df = df[(df['DataDiscriminator'] == 'Order') & (df['Asset Category'] == 'Stocks')]
    
    if stocks_df.empty:
        return None

    result = []
    for _, row in stocks_df.iterrows():
        symbol = row['Symbol']
        date = row['Date/Time'].split(',')[0]
        quantity = float(row['Quantity'])
        price = float(row['T. Price'])
        currency = row['Currency']

        result.append({
            'Symbol': symbol,
            'Date': date,
            'Quantity': quantity,
            'Price': price,
            'Currency': currency
        })

    return pd.DataFrame(result)

def main(folder_name):
    all_data = []
    for file in os.listdir(folder_name):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_name, file)
            df = process_ibkr_csv(file_path)
            if df is not None:
                all_data.append(df)

    if not all_data:
        print("No valid data found in the CSV files.")
        return

    result_df = pd.concat(all_data, ignore_index=True)
    result_df = result_df[['Symbol', 'Date', 'Quantity', 'Price', 'Currency']]
    
    output_file = f'ibkr_{folder_name}.csv'
    result_df.to_csv(output_file, index=False)
    print(f"Aggregated data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py folder_name")
    else:
        main(sys.argv[1])