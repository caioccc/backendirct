import numpy as np
import pandas as pd

from ..const import PATH_FILE, REMOVE_YEAR, DATE_COL


class ExtractData:

    def __init__(self):
        self.path_file = PATH_FILE
        self.remove_year = REMOVE_YEAR

    def break_date(self, date):
        """
        Split date col in day, month and year.

        :param
        (String) date: Column in dataframe that represent date

        :return:
         (Int) day: Represent the day in date
         (Int) month: Represent the month in date
         (Int) year: Represent the year in date
        """
        date_split = date.split('-')
        year, month, day = int(date_split[0]), int(date_split[1]), int(date_split[2])
        return day, month, year

    def extract_data(self):

        """
        Read the csv and convert in  dataframe , add the columns day, month and year in dataframe and
        remove the rows before the constant REMOVE_YEAR(This is stay in const.py)

        :return:
        (Dataframe Pandas) df_result:  Dataframe prepare to use in application.

        """
        df = pd.read_csv(self.path_file, header='infer', sep=';')

        df['day'], df['month'], df['year'] = np.vectorize(self.break_date)(df[DATE_COL])

        df_result = df[df['year'] > REMOVE_YEAR]

        return df_result
