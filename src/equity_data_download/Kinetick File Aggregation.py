import os
import glob
import pandas as pd
from datetime import datetime
from pathlib import PurePath

def read_and_combine_data_files():
    etf_df = pd.DataFrame()

    os.chdir(INPUT_DATA_DIRECTORY)
    file_list = glob.glob("*.csv")

    for filename in file_list:
        print(filename)
        df = pd.read_csv(filename)

        if etf_df.empty:
            etf_df = df.copy()
        else:
            etf_df = pd.merge(etf_df, df, on='Date', how='outer')
    etf_df['Date'] = pd.to_datetime(etf_df['Date'])
    return etf_df.sort_values(by='Date', ascending=False)


def get_inflation_data():
    inflation_df = etf_df[['Date', 'DBC_Close', 'XLB_Close', 'XAU_Close', 'XLF_Close']]
    #print(inflation_df)


def write_excel_file(etf_df):
    print("Generating Excel File")
    writer = pd.ExcelWriter(OUTPUT_EXCEL_FILENAME)
    etf_df.to_excel(writer, 'All Data')
    etf_df.head(1).to_excel(writer, 'Last Day')
    #inflation_df.to_excel(writer, 'Inflation')
    writer.save()


if os.environ['COMPUTERNAME'] == 'SEA-1800100736':
    DATE = '07-12-2018'
    BASE_DIRECTORY = "C:\\Users\\brewshan\\PycharmProjects\\Market_Analysis\\"
    INPUT_DATA_DIRECTORY = BASE_DIRECTORY + "data\\" + DATE + "\\"
    OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
elif os.environ['COMPUTERNAME'] == 'SHANE-TRADING-D':
    #DATE = '07-12-2018'
    DATE = datetime.now().strftime('%m-%d-%Y')
    BASE_DIRECTORY = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\"
    INPUT_DATA_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\" + DATE + "\\"
    OUTPUT_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\"
else:
    DATE = datetime.now().strftime('%m-%d-%Y')
    BASE_DIRECTORY = "D:\\Users\\Shane\\SkyDrive\\Documents\\Trading\\Research\\Data\\"
    INPUT_DATA_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\" + DATE + "\\"
    OUTPUT_DIRECTORY = BASE_DIRECTORY + "Market Analysis Data\\"

OUTPUT_EXCEL_FILENAME = OUTPUT_DIRECTORY + "~priceData.xlsx"

etf_df = read_and_combine_data_files()
#get_inflation_data()
write_excel_file(etf_df)
