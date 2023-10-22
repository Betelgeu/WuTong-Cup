import pandas as pd


class DataProcess:
    def __init__(self, path: str) -> None:
        self.data = pd.read_csv(path)
    
    def process(self):
        self.data = self._data_process(self.data)
        return self.data
    
    @staticmethod
    def _data_process(df: pd.DataFrame):
        df_new = pd.DataFrame()
        data_time_format = "%d-%m月 -%y %H.%M.%S.%f"
        # 拆分出时间和上下午
        df_new['日期时间'] = pd.to_datetime(df['操作时间'].str.rsplit(' ', n=1, expand=True)[0], format=data_time_format)
        # 添加12小时给下午的日期时间
        pm_rows = df['操作时间'].str.endswith("下午")
        time_condition = (df_new['日期时间'].dt.hour != 12)
        df_new.loc[pm_rows & time_condition, '日期时间'] += pd.to_timedelta(12, unit='h')

        df_new['账号'] = df['从账号'].copy()
        df_new['操作内容'] = df['操作内容'].str.slice(36, None).str.strip()
        df_new['源IP'] = df['源IP'].copy()
        df_new = df_new.sort_values(by='日期时间', ascending=True)

        df_new.to_csv('../data_process.csv')

        return df_new
