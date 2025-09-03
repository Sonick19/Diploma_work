import pandas as pd
import json


class Data:

    def __init__(self, data, key, column_categorization):
        self.data = self._check_data_type(data)
        self.keyword = self._check_json_type(key)
        self.categorization = self._check_json_type(column_categorization)

    def _check_data_type(self, data):
        """
        Check if data is path or already a DataFrame and return DataFrame as a result
        :param
            data(str or DataFrame)
        :return:
            DataFrame: full dataset
        """
        if isinstance(data, pd.DataFrame):
            return data
        else:
            return pd.read_csv(data, low_memory=False)

    def _check_json_type(self, data):
        """
        Check if data is path or already a dictionary and return dictionary as a result
        :param
            data(str or dict)
        :return:
            dict: dictionary
        """
        if isinstance(data, dict):
            return data
        else:
            with open(data, 'r', encoding='utf-8') as key_file:
                return json.load(key_file)

    def cat_keys(self):
        """
        return the inline list of possible categorical key,
        which relate to possible column names from dataset
        :return:
            str: list of column name separated by \n
        """
        return '\n'.join(self.keyword.keys())

    def cat_values(self, key):
        """
        return correspondence label for value in a key column

        :param key:
            key(str): The key from self.keyword dictionary, which relate to one of the column from dataset
        :return:
            dict: Key-value pairs for possible meaning in corresponding column
        """

        return self.keyword[key]

    def create_children(self, *columns):
        """
        Create new instance with given dataset by choosing specific columns
        :param columns: list of columns, which should be chosen for new dataset
        :return: new instance with only chosen columns
        """
        return Data(self.data[list(columns)], self.keyword, self.categorization)

    def apply_func(self, func):
        self.data = func(self.data)
