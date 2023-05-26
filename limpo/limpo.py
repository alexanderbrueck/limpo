import pandas as pd
import numpy as np
#from pydataset import data


class Table:
    def __init__(self, dataframe: pd.DataFrame()):
        self.dataframe = dataframe
        self.records = len(self.dataframe)
        self.column_names = self.dataframe.columns

    def find_null_values(self):
        """
        Calculates number and percentage of null values

        Parameters:
            None

        Returns:
            result (pandas.DataFrame or str):
                DataFrame with information about duplicates or str in case there are none.           
        """
        dic = {}

        for col in self.column_names:
            missing = self.dataframe[col].isnull()
            missing_count = np.sum(missing)

            if missing_count > 0:
                dic.update({col: missing_count})

        if dic:
            result = pd.DataFrame.from_dict(dic, orient="index").reset_index()
            result = result.rename(columns={0: "null_values", "index": "column"})
            result["perc_null_values"] = result["null_values"] / self.records
            result = result.sort_values("perc_null_values", ascending=False)
            return result
        else:
            return "No null values found"

    def find_duplicates(self, columns: list):
        """
        Calculates number and percentage of duplicate values

        Parameters:
            columns (list):
                list of column names

        Returns:
            result (pandas.DataFrame):
                DataFrame with information about duplicates            
        """
        dic = {}

        for col in columns:
            series=self.dataframe[col]
            non_null_values = series[~series.isnull()]
            null_values =  sum(series.isnull())
            non_null_values_count = len(non_null_values)
            unique_non_null_values = len(non_null_values.unique())
            dic.update({col: [null_values, non_null_values_count, unique_non_null_values]})

        if dic:
            result = pd.DataFrame.from_dict(dic, orient="index").reset_index()
            result = result.rename(columns={0: "null_values", 1: "non_null_values", 2: "unique_non_null_values", "index": "column"})
            result["duplicates"] = self.records - result["unique_non_null_values"]
            result["percent_duplicates"] = result["duplicates"] / non_null_values_count
        else:
            return "No duplicate values found"    
    
# data = data('cake')
# df = Table(data)
# #print(data)
# #print(df.find_null_values())
# print(df.find_duplicates(["temperature","angle","temp"]))
