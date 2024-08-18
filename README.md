# stock-events-scripts
Scripts to import trades from various brokers into the stock events app. I only have scripts for Wealthsimple and IBKR since that's all that I use.

## Setup
Need to have pandas installed. I recommend the following:

```
python3 -m venv venv
source venv/bin/activate
pip install pandas
```
## Usage
Go to the directory of the broker you want and create a new directory filled with CSVs of the statements you downloaded from each broker. Then run the corresponding main.py file with the folder name as an argument. For Wealthsimple these should be the monthly statements. For IBKR create a custom statement that only reports trades. 

For example

```
stock-events-scripts
|   README.md
|___wealthsimple
|   |___tfsa_statements
|        |   july.csv
|        |   june.csv
|___ibkr
    |___fhsa_statements
        |   july.csv
        |   june.csv

cd wealthsimple
python3 ./main.py tfsa_statements
```
