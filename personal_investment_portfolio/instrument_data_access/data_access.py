import pandas as pd
import logging


class data_access:
   
    def __init__(self):
        pass


    def get_instrument_list_from_csv(self, filename_and_path):
        print("Reading data file: " + filename_and_path)
        check_file_read_permissions(filename_and_path)

        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        df = pd.DataFrame()
        try:
            df = pd.read_csv(filename_and_path)
        except Exception as e:
            print("Error reading CSV file: " + filename_and_path)
        return df
    

    def check_file_read_permissions(self, file):
        try:
            with open(file, 'r') as file:
                logging.info('File has read permissions')
        except IOError as ex:
            logging.error('File ' + str(file) + ' is not readable. Exiting.')
            raise SystemExit
    