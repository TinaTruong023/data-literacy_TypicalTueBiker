import matplotlib.pyplot as plt
from tueplots.constants.color import rgb
import src.Colortheme as ct
import pandas as pd
import numpy as np

COLORS = {
    "schoolbreak":  ct.AREA_COLORS[0],
    "covid_date":   ct.AREA_COLORS[1],
    "holiday":      ct.MARKER_COLORS[0],
    "marker":       rgb.tue_dark,
    "lecture":      [ct.MARKER_COLORS[3],
                     ct.MARKER_COLORS[2]],
}
LINESTYLE = {
    "schoolbreak":  None,
    "covid_date":   None,
    "holiday":      ["-",.8],
    "marker":       [(0, (10, 1)),1],
    "lecture":      [[(0, (10, 1)), "-"],1.1],
}
ALPHAS = {
    "schoolbreak":  0.2,
    "covid_date":   0.4,
    "holiday":      .8,
    "marker":       1,
    "lecture":      .8,
}

def print_holiday_info(info):
    print("Depicted holidays:\n\ {}\n".format(", ".join(info)))

def print_coivd_info(info):
    print(f"Covid-Restrictions:")
    for key in info.keys():
        print(f"\ {key}: {info[key]}\n")

def plot_school_breaks(ed, years, axes, show_label=True, duplicates=True):
    def plot_school_breaks_one_axis(ed, years, ax, show_label):
        data = ed.data["schoolbreak"]
        year_data = data[(data["start"].dt.year.isin(years)) | (data["end"].dt.year.isin(years))]
        show_label = show_label
        for i, row in year_data.iterrows():
            if row["name"] == "Covid-19":
                continue
            legend = "_nolegend_"
            if show_label:
                legend = "School Break"
                show_label = False
            if not row["start"].year in years:
                row["start"] = pd.to_datetime("{}-01-01 00:00:00+00:00".format(min(years)))
            if not row["end"].year in years:
                row["end"] = pd.to_datetime("{}-12-31 23:59:59+00:00".format(max(years)))
            ax.axvspan(
                row["start"].date(),
                row["end"].date(),
                color=COLORS["schoolbreak"],
                alpha=ALPHAS["schoolbreak"],
                zorder=0,
                label=legend
            )
    for i,axis in enumerate(axes):
        lbl = show_label if i > 0 else duplicates
        plot_school_breaks_one_axis(ed, years, axis, lbl)
def plot_holidays(ed, years, axes, all=False, show_label=True, duplicates=True):
    def plot_holidays_one_axis(ed, years, ax, all, show_label):
        data = ed.data["holiday"]
        year_data = data[data["start"].dt.year.isin(years)]
        # choose days that are not Sundays and of category 1, 2 or 3 and not these particular days
        exclude_holidays = ["Zweiter Weihnachtsfeiertag", "Heiliger Abend", "Neujahr"]
        if not all:
            year_data = year_data[(~year_data["holiday"].isin(exclude_holidays)) & (year_data["day"] != "Sunday") & (year_data["class"].isin([1, 2, 3]))]
        show_label = show_label
        for i, row in year_data.iterrows():
            legend = "_nolegend_"
            if show_label:
                legend = "Holiday"
                show_label = False
            ax.axvline(
                row["start"].date(),
                color=COLORS["holiday"],
                lw=LINESTYLE["holiday"][1],
                ls=LINESTYLE["holiday"][0],
                alpha=ALPHAS["holiday"],
                # zorder=2,
                label=legend
            )
        return year_data["holiday"].tolist()
    holidays = None
    for i,axis in enumerate(axes):
        lbl = show_label if i > 0 else duplicates
        holidays = plot_holidays_one_axis(ed, years, axis, all, lbl)
    return holidays

def plot_marker(marker, axes):
    def plot_marker_in_one_axis(marker, ax):
        if marker is not None:
            for marker in marker:
                ax.axvline(
                    marker.date(),
                    color=COLORS["marker"],
                    lw=LINESTYLE["marker"][1],
                    alpha=ALPHAS["marker"]-0.2,
                    zorder=2
                )
                ax.text(
                    marker.date(),
                    ax.get_ylim()[0]+0.02 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                    s=marker.strftime("%d.%m"),
                    color=ct.PRIMARY_COLORS[0],
                    rotation=90,
                    zorder=10
                )
    [plot_marker_in_one_axis(marker, axis) for axis in axes]

def plot_covid(ed, years, axes, show_label=True, show_abbr=True):
    def plot_covid_one_axis(ed, years, ax, show_label, show_abbr):
        data = ed.data["covid_date"]
        info = ed.data["covid_info"]
        year_data = data[(data["type"] == "Lockdown") & ((data["start"].dt.year.isin(years)) | (data["end"].dt.year.isin(years)))]
        description_dict = {}
        show_label = show_label
        for i, row in year_data.iterrows():
            legend = "_nolegend_"
            if show_label:
                legend = "Covid Restrictions"
                show_label = False
            if not row["start"].year in years:
                row["start"] = pd.to_datetime("{}-01-01 00:00:00+00:00".format(min(years)))
            if not row["end"].year in years:
                row["end"] = pd.to_datetime("{}-12-31 23:59:59+00:00".format(max(years)))
            ax.axvspan(
                row["start"].date(),
                row["end"].date(),
                color=COLORS["covid_date"],
                alpha=ALPHAS["covid_date"],
                zorder=0,
                label=legend
            )
            if show_abbr == True:
                ax.text(
                    row["start"].date(),
                    ax.get_ylim()[0] + 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                    s=row["id"],
                    color=COLORS["covid_date"]*(0.5,0.5,0.5),
                    rotation=90,
                    # zorder=10
                )
            description_dict[row["id"]] = info.loc[info["id"] == row["id"], "information"].values[0]
        return description_dict
    return [plot_covid_one_axis(ed, years, axis, show_label, show_abbr) for axis in axes][0]


def plot_lecture_period(ed, years, axes, show_label=True, duplicates=True, no_lbl=False):
    def plot_lecture_period_axis(ed, years, ax, show_label, no_lbl=False):
        data = ed.data["lecture"]
        year_data = data[(data["start"].dt.year.isin(years)) | (data["end"].dt.year.isin(years))]
        show_label_1 = show_label
        show_label_2 = show_label
        for year in years:
            for i, row in year_data.iterrows():
                legend = "_nolegend_"
                if row["start"].year == year:
                    if show_label_1:
                        legend = "SoSe" if "SS" in row["semester"] else "WiSe"
                        show_label_1 = False
                    ax.axvline(
                        row["start"].date(),
                        color=COLORS["lecture"][0] if "WS" in row["semester"] else COLORS["lecture"][1],
                        lw=LINESTYLE["lecture"][1],
                        linestyle=LINESTYLE["lecture"][0][0],
                        alpha=ALPHAS["lecture"],
                        zorder=2,
                        label=legend
                    )
                    ax.text(
                        row["start"].date(),
                        ax.get_ylim()[0]+0.06 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                        s="LStart",#if "SS" in row["semester"] else "SoSe",
                        color=COLORS["lecture"][0] if "WS" in row["semester"] else COLORS["lecture"][1],
                        rotation=90,
                        zorder=10
                    )
                legend = "_nolegend_"
                if row["end"].year == year:
                    if show_label_2:
                        legend = "SoSe" if "SS" in row["semester"] else "WiSe"
                        show_label_2 = False
                    ax.axvline(
                        row["end"].date(),
                        color=COLORS["lecture"][1] if "SS" in row["semester"] else COLORS["lecture"][0],
                        lw=LINESTYLE["lecture"][1],
                        linestyle=LINESTYLE["lecture"][0][1],
                        alpha=ALPHAS["lecture"],
                        zorder=2,
                        label=legend
                    )
                    ax.text(
                        row["end"].date(),
                        ax.get_ylim()[0]+0.06 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                        s="LEnd",#"WiSe" if "SS" in row["semester"] else "SoSe",
                        color=COLORS["lecture"][1] if "SS" in row["semester"] else COLORS["lecture"][0],
                        rotation=90,
                        zorder=10
                    )
        return 1

    no_lbl = True
    for i,axis in enumerate(axes):
        lbl = show_label if i > 0 else duplicates

        plot_lecture_period_axis(ed, years, axis, lbl )