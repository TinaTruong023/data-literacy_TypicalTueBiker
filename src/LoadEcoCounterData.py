import pandas as pd
import os
pd.set_option('display.max_columns', None)


class EcoCounterData:
    """
    Provides eco counter data for given years.
    """
    AVB_YEARS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]

    def __init__(self):
        # extract data from csvs
        df_list = []
        src_dir = os.path.join(os.path.dirname(__file__), "..", "dat", "eco")
        for f in os.listdir(src_dir):
            if f.startswith("eco") and f.endswith(".csv"):
                df_list.append(pd.read_csv(os.path.join(src_dir, f), parse_dates=["iso_timestamp"]))

        # create dataframe
        self.df_uncorrected = pd.concat(df_list).reset_index()
        self.df_uncorrected.sort_values(by=["iso_timestamp"], inplace=True)

        # convert to local time
        self.df_uncorrected['iso_timestamp'] = self.df_uncorrected['iso_timestamp'].dt.tz_convert('Europe/Berlin')

        # apply calendar week and weekday to dataframe
        self.df_uncorrected["calendar_week"] = self.df_uncorrected["iso_timestamp"].dt.isocalendar().week
        self.df_uncorrected["weekday"] = self.df_uncorrected["iso_timestamp"].dt.weekday

        # correct data by removing days for one counter with zählstand sum zero
        grouped = self.df_uncorrected.groupby([self.df_uncorrected["iso_timestamp"].dt.date,
                                               "channel_name",
                                               "channel_id",
                                               "counter_site",
                                               "counter_site_id",
                                               "calendar_week",
                                               "weekday"
                                               ])
        filtered = {date: group for date, group in grouped if group["zählstand"].sum() != 0}
        self.df_corrected = pd.concat(filtered.values())  # .reset_index()

        # create daily sum df for both categories
        self.df_uncorrected_daily = self.df_uncorrected.groupby([self.df_uncorrected["iso_timestamp"].dt.date,
                                                                 "counter_site",
                                                                 "counter_site_id",
                                                                 "calendar_week",
                                                                 "weekday"
                                                                 ])["zählstand"].sum().reset_index()
        self.df_uncorrected_daily["iso_timestamp"] = pd.to_datetime(self.df_uncorrected_daily["iso_timestamp"])
        self.df_corrected_daily = self.df_corrected.groupby([self.df_uncorrected["iso_timestamp"].dt.date,
                                                             "counter_site",
                                                             "counter_site_id",
                                                             "calendar_week",
                                                             "weekday"
                                                             ])["zählstand"].sum().reset_index()
        self.df_corrected_daily["iso_timestamp"] = pd.to_datetime(self.df_corrected_daily["iso_timestamp"])

    def get_hourly_data(self, years=None, counter_id=None, corrected=True, time_as_index=False):
        """
        Get hourly data for given years in local time.
        :param years: list of years
        :param counter_id: list of counter ids, if None all counters are returned
        :param corrected: boolean, if True corrected data is returned, else uncorrected data
        :param time_as_index: boolean, if True index is set to iso_timestamp
        """
        if years is None:
            years = self.AVB_YEARS
        year_data = self.df_uncorrected[self.df_uncorrected["iso_timestamp"].dt.year.isin(years)]
        if corrected:
            year_data = self.df_corrected[self.df_corrected["iso_timestamp"].dt.year.isin(years)]
        if counter_id is not None:
            year_data = year_data[year_data["counter_site_id"].isin(counter_id)]
        if time_as_index:
            year_data.set_index("iso_timestamp", inplace=True)
        return year_data

    def get_daily_data(self, years=None, counter_id=None, corrected=True, time_as_index=False):
        """
        Get daily data for given years in local time.
        :param years: list of years
        :param counter_id: list of counter ids, if None all counters are returned
        :param corrected: boolean, if True corrected data is returned, else uncorrected data
        :param time_as_index: boolean, if True index is set to iso_timestamp
        """
        if years is None:
            years = self.AVB_YEARS
        year_data = self.df_uncorrected_daily[self.df_uncorrected_daily["iso_timestamp"].dt.year.isin(years)]
        if corrected:
            year_data = self.df_corrected_daily[self.df_corrected_daily["iso_timestamp"].dt.year.isin(years)]
        if counter_id is not None:
            year_data = year_data[year_data["counter_site_id"].isin(counter_id)]
        if time_as_index:
            year_data.set_index("iso_timestamp", inplace=True)
        return year_data

    def get_df(self, years):
        """
        -- DEPRECATED --
        Just use get_hourly_data or get_daily_data instead. This method is kept for compatibility reasons.
        Get data for given years.
        :param years: list of years
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

        df['iso_timestamp'] = df['iso_timestamp'].dt.tz_convert('Europe/Berlin')
        # cut out previous year remainders
        self.df_uncorrected = df[df["iso_timestamp"].dt.year.isin(years)]


if __name__ == "__main__":
    bd = EcoCounterData()
    df = bd.get_daily_data()
    print(df.head())
