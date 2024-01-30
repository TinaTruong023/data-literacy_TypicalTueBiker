import pandas as pd
import matplotlib.dates as mdates
import src.Colortheme as ct
import numpy as np
from tueplots import bundles

COUNTER = {
    100003358: {
        'name': 'Fahrradtunnel',
        'color': ct.COUNTER_COLORS[0],
        'marker': '.',
    },
    100003359: {
        'name': 'Unterführung Steinlachallee',
        'color': ct.COUNTER_COLORS[1],
        'marker': '.',
    },
    100026408: {
        'name': 'Radweg Hirschau',
        'color': ct.COUNTER_COLORS[2],
        'marker': '.',
    },
    "FSC": {'color': ct.COUNTER_COLORS[3], 'name': 'Fahrradtunnel & Unterführung Steinlachallee'},
}
COUNTER_ORDER = [100003358, 100003359, 100026408, "FSC"]
WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
LEGEND_COUNTER_ORDER = {
    "standard": [0,1,2,3,5,4],
    "covid_standard": [0,1,2,4,3,5],
    "uncorrected": [0,1,2,3,5,4],
    "covid_uncorrected": [0,1,2,3,5,6,4]
}
COUNT_STYLE = {
    "c": ct.PRIMARY_COLORS[0],
    "m": ".", "ms":1.2,
    "ls": "-", "lw": 0.8,
    "a": 0.45,
}
ROLLING_WINDOW_STYLE = {
    "c": COUNT_STYLE["c"],
    "m": None, "ms":None,
    "ls": "-", "lw": 1.5,
    "a": 0.85,
}
NOTEBOOK_FACTOR = 1.4
AXIS_TITLE_PARAMS = {
    "loc": "left"
}
DECOMP_STYLE = {
    "c": None,
    "m": None, "ms":None,
    "ls": "-", "lw": [1,1.5,1,1],
    "a": 0.6, "xlabel": "Day",
}

FIGURE_STYLE = {
    4: bundles.beamer_moml(rel_width=1.8,rel_height=2.4),
    3: None
}

def set_tick_locator(ax, mode, interval=1):
    """
    Set tick locator for x-axis.
    :param ax: axis to set locator for
    :param mode: mode for locator, one of ["hour", "day", "week", "month", "year"]
    :param interval: interval for ticks
    """
    if mode == "hour":
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    if mode == "day":
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    if mode == "week":
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
    if mode == "month":
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=interval))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    if mode == "year":
        ax.xaxis.set_major_locator(mdates.YearLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

def plot_daily_per_counter(daily_bike_dfs, avb_counter, year, figure_obj,
                           rolling_window=None):
    """
    Plot daily bike counts per counter for a given year.
    :param daily_bike_dfs: list of dataframes with daily bike counts (corrected and uncorrected).
    :param year: year to plot
    :param figure_obj: contains figure and axis to furhter plot on
    :param rolling_window: rolling window for smoothing
    """
    df_year = daily_bike_dfs[0]
    df_year_uncorrected = daily_bike_dfs[1]

    max_per_counter = [
        df_year[df_year["counter_site_id"]==COUNTER_ORDER[i]]["zählstand"].max()
        for i in range(3)
    ]
    y_lims_per_counter = [max_per_counter[1]+1200, max_per_counter[1]+1200, max_per_counter[2]+500]
    # y_lims_per_counter = [13000, 13000, 6000]
    if df_year.empty:
        print("No data for year {}".format(year))
        return
    filtered_counters = [c for c in COUNTER_ORDER if c in avb_counter]
    fig, ax = figure_obj
    comp_legend = ["Counted Bikes Per Day", ""]
    # compute rolling mean per counter and plot
    for i, counter in enumerate(filtered_counters):
        df_counter_year = df_year[df_year["counter_site_id"] == counter].copy()
        df_counter_year_uncorrected = df_year_uncorrected[df_year_uncorrected["counter_site_id"] == counter]
        rw_data = df_counter_year.copy()
        if rolling_window is not None:
            # apply rolling window
            rw_data.index = pd.to_datetime(rw_data.index)
            rw_data['smoothed'] = rw_data['zählstand'].rolling(window=rolling_window).mean()

        if df_counter_year.shape[0] != df_counter_year_uncorrected.shape[0]:
            color_fac = 0.6
            uncorrected_color = COUNTER[counter]["color"]*[color_fac,color_fac,color_fac]
            ax[i].plot(
                df_counter_year_uncorrected.index.date,
                df_counter_year_uncorrected["zählstand"],
                color=uncorrected_color,
                label="Uncorrected Counted Bike per Day",
                linestyle=(0,(1,1)),
                ms=2, lw=1.5,
                alpha=0.3
            )
        # !LINE PLOT!
        ax[i].plot(
            df_counter_year.index, df_counter_year["zählstand"],
            marker=COUNT_STYLE["m"], ms=COUNT_STYLE["ms"]*NOTEBOOK_FACTOR,
            ls=COUNT_STYLE["ls"], lw=COUNT_STYLE["lw"]*NOTEBOOK_FACTOR,
            alpha=COUNT_STYLE["a"]+0.05,
            color=COUNTER[counter]["color"]*0.9,
            label="Daily Counted Bikes"
        )

        if rolling_window is not None:
            ax[i].plot(
                rw_data.index.date, rw_data["smoothed"],
                lw=ROLLING_WINDOW_STYLE["lw"]*NOTEBOOK_FACTOR,
                alpha=ROLLING_WINDOW_STYLE["a"],
                color=COUNTER[counter]["color"],
                label=f"{rolling_window}-Day-Rolling-Mean"
            )
        # custom_leg = [(line_aura), "Bike count per day"]
        # ax[i].legend([(line_aura, mark)], ['Bike count per day'])
        # Set the x-axis ticks to be in months
        ax[i].set_title(f"{COUNTER[counter]['name']}", loc=AXIS_TITLE_PARAMS["loc"])
        ax[i].set_xlim([pd.Timestamp(f"{year}-01-01").date(), pd.Timestamp(f"{year}-12-31").date()])
        ax[i].set_ylim(bottom=0, top=y_lims_per_counter[i])
        set_tick_locator(ax[i], "month")
        ax[i].xaxis.set_minor_locator(mdates.WeekdayLocator())
        # ax[i].xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax[i].grid(axis="x", which="major", ls="-", alpha=0.3)
        ax[i].grid(axis="x", which="minor", ls=":", alpha=0.25)
        ax[i].grid(axis="y", which="major", ls=":", alpha=0.2)
        ax[i].set_ylabel("Bike Count")
    ax[-1].set_xlabel("Time (in Days)")
    fig.suptitle(f"Daily Bike Counts per Counter in {year}")
    fig.align_labels()
    # return custom_leg

def plot_seasonal_decomposition(decomp_obj, figinfo,
                                counter_id=None,
                                show_window=None,
                                xtick_format="month",
                                combine_counters=None
                                ):
    week_view = xtick_format == "week"
    decomposition_elements, decomposition_element_index = decomp_obj
    d_years = [2014, 2023]
    min_year = decomposition_elements[0].index.year.min()
    years = [year for year in range(min_year, 2024)]
    if counter_id[0] == 100026408:
        years = list(set(years) - set([2014,2015]))
        d_years = [2016,2023]
    fig, ax = figinfo
    line_w_factor = 1 if week_view else 0

    for i, data in enumerate(decomposition_elements):
        ax[i].plot(
            data.index, data,
            marker='.' if week_view else None, ms=4,
            alpha=DECOMP_STYLE["a"],
            linestyle=DECOMP_STYLE["ls"], lw=DECOMP_STYLE["lw"][i]+line_w_factor,
            color=COUNTER[counter_id[0]]["color"] if not combine_counters else COUNTER["FSC"]["color"],
        )
        if show_window is not None:
            years = [show_window[0].year, show_window[1].year]

        if show_window is None:
            show_window = [pd.Timestamp(f"{min(years)}-01-01").date(), pd.Timestamp(f"{max(years)}-12-31").date()]
        ax[i].set_xlim(show_window)
        if week_view:
            ax[i].xaxis.set_major_locator(mdates.DayLocator(interval=2 if not combine_counters else 1))
            ax[i].xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
        else:
            ax[i].xaxis.set_minor_locator(mdates.MonthLocator())
        ax[i].grid(axis="x", which="major", ls="-", alpha=1)
        if week_view:
            ax[i].grid(axis="x", which="minor", ls=":", alpha=0.3)
            ax[i].grid(axis="y", which="major", ls="-", alpha=0.2)

        ax[i].set_ylabel("Bike Count")
        if i<2:
            pass
        else:
            ax[i].axhline(0, color="black", alpha=0.2, lw=1)
            if counter_id[0] != COUNTER_ORDER[2] or i == 3:
                y_offset = 100 if show_window is not None else 250
                # y_offset = 250
                mag = -2 if show_window is not None else -3
                abs_max = abs(round(max(data.max(), data.min(), key=abs),mag))
                ylims = (-abs_max, abs_max)
                ax[i].set_ylim(ylims[0]-y_offset, ylims[1]+y_offset)
                ax[i].set_yticks(np.linspace(ylims[0], ylims[1], 5))

        ax[i].set_title(decomposition_element_index[i], loc=AXIS_TITLE_PARAMS["loc"])


    ylims = (0, round(decomposition_elements[0].max(), -3))
    y_offset = 1000 if counter_id[0] != COUNTER_ORDER[2] else 100
    ax[0].set_ylim(ylims[0], ylims[1]+y_offset if week_view else ylims[1]+y_offset)
    # if week_view:
    #         ax[1].set_ylim(ylims[0], ylims[1]+1000)
    ax[0].set_yticks(np.linspace(ylims[0], ylims[1], 5))
    if counter_id[0] == COUNTER_ORDER[2] and week_view:
        ylims = [-200,200]
        ax[2].set_ylim(ylims[0], ylims[1])
        ax[2].set_yticks(np.linspace(ylims[0], ylims[1], 5))
    ax[-1].set_xlabel(DECOMP_STYLE["xlabel"])
    fig.align_labels()

    if counter_id is None:
        fig.suptitle("Seasonal Decomposition of Summed Bike Counts in Tübingen ({} - {})".format(min(d_years), max(d_years)))
    else:
        if len(counter_id) == 1:
            if week_view:
                fig.suptitle(f"Weekly Trend on {COUNTER[counter_id[0]]['name']}: Winodwed View on {show_window[0].strftime('%B')} in {show_window[0].strftime('%Y')}",)
            else:
                fig.suptitle(f"Seasonal Decomposition of Summed Bike Counts in Tübingen for Counter {COUNTER[counter_id[0]]['name']} ({min(d_years)} - {max(d_years)})",)
        else:
            fig.suptitle(f"Seasonal Decomposition of Summed Bike Counts in Tübingen\nfor Counters {combine_counters} ({min(d_years)} - {max(d_years)})")

def plot_avg_weekday(wd_data, weekday, figinfo, years=None, counter_id=None,
                     plot_directions=False, ymax=None):
    weekday_mean, in_mean, out_mean = wd_data
    combined_counter = "FSC" if len(counter_id)>1 else None
    selected_counter_settings = COUNTER[combined_counter] if combined_counter is not None else COUNTER[counter_id[0]]
    fig, ax = figinfo

    # !Counter Line!
    selected_counter_settings = COUNTER[combined_counter] if combined_counter is not None else COUNTER[counter_id[0]]
    ax.plot(
        weekday_mean.index,
        weekday_mean,
        lw=1.5,
        alpha=0.8,
        color=selected_counter_settings["color"],
        label="Mean Count"
    )

    if plot_directions:
        ax.plot(
            in_mean.index,
            in_mean,
            color=ct.PRIMARY_COLORS[1],
            ls=(0, (1, 1)),
            label="Mean Count: To Tübingen"
        )
        ax.plot(
            out_mean.index,
            out_mean,
            ls=(0, (1, 1)),
            color=ct.AREA_COLORS[2],
            label="Mean Count: From Tübingen"
        )
    counter_names = "All Tübingen Counters"
    if counter_id is not None:
        counter_names = "+".join([COUNTER[c]["name"] for c in counter_id])
    year_span = "(2014 - 2023)"
    if years is not None:
        year_span = "({} - {})".format(min(years), max(years))
    ax.set_title("Mean Count per Hour @ {} for Weekday {} {}".format(counter_names, WEEKDAYS[weekday], year_span))#loc=AXIS_TITLE_PARAMS["loc"])
    ax.set_xlabel("Time of Day")
    ax.set_ylabel("Mean Counted Bikes")
    ax.set_xticks(range(0, 24, 1))
    ax.grid()
    ax.set_xlim(0, 23)
    if ymax:
        ax.set_ylim(bottom=0, top=ymax)
    else:
        ax.set_ylim(bottom=0)
    ax.set_xticklabels(["{:02d}h".format(i) for i in range(0, 24, 1)])
    ax.legend(bbox_to_anchor=(0,1), ncol=1, loc="upper left", frameon=True)