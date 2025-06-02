import pandas as pd

class Course:
    def __init__(self, path: str):
        self.df = pd.read_csv(path)