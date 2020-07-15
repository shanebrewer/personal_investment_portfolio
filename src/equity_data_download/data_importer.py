import pandas as pd
import time
from datetime import datetime, timedelta


class data_importer:  
    def __init__(self):
        pass


    def read_equity_list_from_csv(self, filename_and_path):
        print("Reading data file: " + filename_and_path)
        df = pd.read_csv(filename_and_path)
        return df
    