import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

def resampling_data(bikedata, counter_id=None, resample_mean=False):
    """
    Resample data for seasonal decomposition.
    :param bikedata: data to resample
    :param years: list of years to plot
    :param counter_id: list of counter ids, if None all counters are returned
    :param resample_mean: whether to resample with mean or sum
    :return: resampled data
    """
    df = bikedata
    if counter_id is not None:
        df = df[df["counter_site_id"].isin(counter_id)]

    df_resampled = df.resample('D').sum()
    if resample_mean:
        df_data_reduced = df[["zählstand", "weekday"]].copy()
        df_resampled = df_data_reduced.resample('D').mean()
    return df_resampled

def get_seasonal_decomposition(df, counter_id, years=None, week_view=False, show_window=False,
                               corr=False, residuals=False, resample_mean=False,):
    """Creates the seasonal decomposition of the data.
    :param df: data to plot
    :param week_view: whether to plot the weekly view
    :param show_window: whether to show the window
    :param period: period of the seasonal decomposition
    :return: list containing (0) seasonal decomposition (1) their labels
    """
    if corr:
        counter = {
            100003358:"zählstand_tunnel",
            100003359:"zählstand_steinlach",
            100026408:"zählstand_hirschau",
        }
        df_custom = df
        df_custom.set_index("iso_timestamp", inplace=True)
        data_process = df[counter[counter_id[0]]]
    else:
        df_resampled = resampling_data(df, counter_id, resample_mean=resample_mean)
        data_process = df_resampled["zählstand"]
    period = 7 if week_view else 365
    decomposition = seasonal_decompose(data_process, model='additive', period=period, two_sided=False)
    decomposition_elements = [decomposition.observed, decomposition.trend, decomposition.seasonal]
    if residuals:
        decomposition_elements.append(decomposition.resid)
    decomposition_element_index = [f"Counts per Day", f"Trend by {period}-Day Mean", "Seasonal Component", "Residuals"]
    if week_view:
        decomp_zoomed = []
        for decomp in decomposition_elements:
            dec_z = decomp.copy()
            dec_z = dec_z[dec_z.index.year == show_window[0].year]
            dec_z = dec_z[dec_z.index.month == show_window[0].month]
            decomp_zoomed.append(dec_z)
        decomposition_elements = decomp_zoomed
    return [decomposition_elements, decomposition_element_index]