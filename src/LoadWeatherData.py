import pandas as pd
pd.set_option('display.max_columns', None)
import os


class WeatherCounterData:
    """
    Provides eco counter data for given years.
    """
    def __init__(self):
        self.year_dfs = {}

        src_dir = os.path.join(os.path.dirname(__file__), "..", "dat", "wea")
        for f in os.listdir(src_dir):
            if f.startswith("wea_") and f.endswith(".csv"):
                year = f.split("_")[1].split(".")[0]
                df = pd.read_csv(os.path.join(src_dir, f), parse_dates=["timestamp"])
                df.rename(columns={"timestamp": "iso_timestamp", "Tübingen Temperature [2 m elevation corrected]": "temperature", "Tübingen Precipitation Total": "precipitation"}, inplace=True)
                self.year_dfs[year] = df
        #print("loaded dataframes for years: {}".format(list(self.year_dfs.keys())))

    def get_df(self, years, to_local_time=False):
        """
        Get data for given years. If to_local_time is True, the iso_timestamp column is converted to local time.
        :param years: list of years
        :param to_local_time: boolean
        :return: dataframe of combined years
        """
        data_list = []
        # get last day of previous year
        if int(years[0]) > 2013:
            prev_year = str(int(years[0]) - 1)
            prev_year_df = self.year_dfs[prev_year]
            prev_year_last_day = prev_year_df.iloc[-1]["iso_timestamp"].date()
            data_list.append(prev_year_df[prev_year_df["iso_timestamp"].dt.date == prev_year_last_day])

        # get data for each year
        for y in years:
            data_list.append(self.year_dfs[str(y)])

        # concatenate dateframes
        df = pd.concat(data_list)
        df.sort_values(by=['iso_timestamp'], inplace=True)
        df["iso_timestamp"] = pd.to_datetime(df["iso_timestamp"], utc=True)

        if to_local_time:
            df['iso_timestamp'] = df['iso_timestamp'].dt.tz_convert('Europe/Berlin')
        return df


if __name__ == "__main__":
    bd = WeatherCounterData()
    df = bd.get_df([2019,2017])
    print(df.head())