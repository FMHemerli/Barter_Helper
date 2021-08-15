import gspread as gs
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('barter-analyser-957533c4bc5c.json', scope)
client = gs.authorize(creds)

sheet = client.open("Barter Calculator")
tab = sheet.worksheet("Barter Calculator")
dataset = pd.DataFrame(tab.get_all_records())

land_goods = dataset[['ID', 'Item', 'Market Price', 'Amount x1', 'Amount x6', 'MP Amt', 'Cost/silver per 6 LV 1']]
land_goods.rename(
    columns={
        'Cost/silver per 6 LV 1': 'Total Cost',
        'Amount x1': 'Amount per Trade',
        'Amount x6': 'Amount per Route',
        'MP Amt': 'Availability'
    }, inplace=True)

land_goods.loc[:, ['Market Price']] = land_goods['Market Price'].apply(
    lambda x: str(x).replace(',', '')).astype(int)
land_goods.loc[:, ['Total Cost']] = land_goods['Total Cost'].apply(
    lambda x: str(x).replace(',', '')).astype(int)
land_goods.loc[:, ['Amount per Route']] = land_goods['Amount per Route'].apply(
    lambda x: str(x).replace(',', '')).astype(int)
land_goods.loc[:, ['Availability']] = land_goods['Availability'].apply(
    lambda x: str(x).replace(',', '')).astype(int)

land_goods.to_json("Barter.json", orient='records')
land_goods.set_index('ID').to_csv("Barter.csv")
