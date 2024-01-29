import pandas as pd
pd.set_option('display.max_columns', None)
import os


class FuelData:
    """
    Provides eco counter data for given years.
    """
    def __init__(self): # TODO: hourly and not avg_hourly right?
        file_n = "fue_price_data_tue_hourly.csv"
        data_path = os.path.join(os.path.dirname(__file__), "..", "dat", "fue", file_n)
        self.df = pd.read_csv(data_path, parse_dates=["iso_timestamp"])
        self.df['iso_timestamp'] = pd.to_datetime(self.df['iso_timestamp'], utc=True)

    def get_df(self, years, to_local_time=False):
        """
        Get data for given years. If to_local_time is True, the iso_timestamp column is converted to local time.
        :param years: list of years
        :param to_local_time: boolean
        :return: dataframe of combined years
        """

        data = self.df[self.df["iso_timestamp"].dt.year.isin(years)].copy()
        data.reset_index(inplace=True, drop=True)

        data["iso_timestamp"] = pd.to_datetime(data["iso_timestamp"], utc=True)

        if to_local_time:
            data['iso_timestamp'] = data['iso_timestamp'].dt.tz_convert('Europe/Berlin')
        return data


if __name__ == "__main__":
    bd = FuelData()
    df = bd.get_df([2018, 2019])
    print(df.head())