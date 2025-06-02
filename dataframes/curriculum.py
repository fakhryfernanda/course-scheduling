import pandas as pd
import numpy as np

class Curriculum:
    def __init__(self, path: str, subjects: pd.DataFrame, courses: pd.DataFrame):
        self.df = pd.read_csv(path)

        sessions = self.get_session_durations(courses)
        self.df = self.df.merge(sessions, left_on='id', right_on='curriculum_id', how='left')
        self.df.drop(columns=['curriculum_id'], inplace=True)

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

    def get_session_durations(self, courses: pd.DataFrame) -> pd.DataFrame:
        """
        For each curriculum_id, return a DataFrame with session_1 and session_2 durations.
        Ensures session_1 >= session_2 by swapping values if needed.

        Returns:
        - pd.DataFrame: with columns ['curriculum_id', 'session_1', 'session_2']
        """
        session_df = (
            courses.pivot_table(index="curriculum_id", columns="session", values="duration", aggfunc="first")
            .fillna(0)
            .astype(int)
            .rename(columns={1: "session_1", 2: "session_2"})
            .reset_index()
        )

        # Ensure session_1 >= session_2
        session_df[["session_1", "session_2"]] = session_df[["session_1", "session_2"]].apply(
            lambda row: sorted(row, reverse=True), axis=1, result_type="expand"
        )

        return session_df
    
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
    
    