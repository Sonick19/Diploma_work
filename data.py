import pandas as pd


class Data:
    def __init__(self, path, key, column_categorization):
        self.data = pd.read_csv(path, low_memory=False)
        self.key = key
        self.categorization = column_categorization
