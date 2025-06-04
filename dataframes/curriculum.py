import pandas as pd
import numpy as np

class Curriculum:
    def __init__(self, path: str, subjects: pd.DataFrame):
        self.df = pd.read_csv(path)

        # Merge with subjects, suffixing overlapping columns clearly
        self.df = self.df.merge(subjects, left_on='subject_id', right_on='id', how='left', suffixes=('_curr', '_subj'))

        # Drop redundant subject id
        self.df.drop(columns=['id_subj'], inplace=True)

        # Rename for clarity
        self.df.rename(columns={
            'id_curr': 'id',
            'code': 'subject_code',
            'subject': 'subject_name'
        }, inplace=True)
    
    def get_classes_map(self, session: int, duration: int) -> dict:
        """
        Returns a dictionary where the key is curriculum_id (id),
        and the value is classes, for rows where session_1 == 2.
        
        Parameters:
        - df (pd.DataFrame): Must include 'id', 'session_1', and 'classes' columns.
        
        Returns:
        - dict: {curriculum_id: classes}
        """
        key = "session_1" if session == 1 else "session_2"

        return (
            self.df[self.df[key] == duration]
            .set_index("id")["classes"]
            .to_dict()
        )
    
    