"""
This module contains functions to make diagnostic plots of the ``AMPEL`` run.

* :func:`chunk_distribution_plots` plots the number of analysed objects and the distribution of statuses among chunks.
* :func:`positional_outliers` plots the times of positional outliers.
* :func:`color_change` plots the change of magnitudes between the cataloged magnitudes and the magnitudes calculated
* :func:`strength_vs_color` plots the strength of the candidates vs the color change.
* :func:`plot_separation` plots the separation of the flare position from the baseline position for a given object.
"""

import logging
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from astropy.time import Time
from pathlib import Path
from timewise.wise_data_base import WISEDataBase
from timewise import WiseDataByVisit

from timewise_sup.plots import plots_dir
from timewise_sup.mongo import Index, DatabaseConnector
from timewise_sup.meta_analysis.diagnostics import (
    get_statuses_per_chunk,
    get_catalog_matches_per_chunk,
    get_positional_outliers_times,
    get_baseline_changes,
    get_baseline_change_fit,
    cutoff_model
)
from timewise_sup.meta_analysis.separation import get_separation


logger = logging.getLogger(__name__)


def chunk_distribution_plots(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase
):
    """
    Make diagnostic plots of the chunk distribution. This includes the number of analysed objects per chunk and the
    distribution of statuses among chunks.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    """
    logger.info(f"making chunk distribution diagnostic plots for {base_name}")
    d = plots_dir("diagnostics", base_name)

    # --- plot analyses stocks per chunk ---#

    statuses = get_statuses_per_chunk(base_name, database_name, wise_data)

    logger.info("plotting number of analysed objects")
    n_stocks = {c: len(v) for c, v in statuses.items()}
    fig, ax = plt.subplots()
    ax.bar(np.array(list(n_stocks.keys())).astype(int), n_stocks.values())
    ax.set_xlabel("chunk number")
    ax.set_ylabel("# of analysed objects")
    for loc in ["top", "right"]:
        ax.spines[loc].set_visible(False)

    ax.grid(ls=":", alpha=0.5)

    fig.tight_layout()
    fn = os.path.join(d, "number_per_chunk.pdf")
    logger.debug(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()

    # --- plot distribution of statuses among chunks ---#

    logger.info("plotting status distribution among chunks")
    _unique_statuses = [
        "1",
        "1_maybe_interesting",
        "2",
        "2_maybe_interesting",
        "3",
        "3_maybe_interesting",
        "4",
        "4_maybe_interesting",
        "No further investigation"
    ]

    n_status = dict()
    for s in _unique_statuses:
        logger.debug(f"getting # of objects for {s}")
        in_status = dict()
        for c, istatus in statuses.items():
            in_status[c] = np.sum(np.array(istatus) == s)

        n_status[s] = in_status

    for s, in_status in n_status.items():
        logger.debug(f"plotting {s}")
        fig, ax = plt.subplots()
        ax.bar(np.array(list(in_status.keys())).astype(int), list(in_status.values()))
        ax.grid(ls=":", alpha=0.5)
        ax.set_xlabel("chunk number")
        ax.set_ylabel("# of objects")
        ax.set_title(s)
        for loc in ["top", "right"]:
            ax.spines[loc].set_visible(False)

        fig.tight_layout()
        fn = os.path.join(d, f"number_per_chunk_status_{s}.pdf")
        logger.debug(f"saving under {fn}")
        fig.savefig(fn)
        plt.close()

    # --- plot distribution of catalogue matches among chunks --- #

    number_of_catalogue_matches = pd.DataFrame.from_dict(
        get_catalog_matches_per_chunk(base_name, database_name, wise_data),
        orient="index"
    ).fillna(0)

    fig, ax = plt.subplots()

    bottom = None
    for i, c in enumerate(number_of_catalogue_matches.columns):
        bottom = (
            0 if i == 0 else
            bottom + number_of_catalogue_matches[number_of_catalogue_matches.columns[i - 1]]
        )
        ax.bar(
            number_of_catalogue_matches.index,
            number_of_catalogue_matches[c],
            bottom=bottom,
            label=c
        )

    for loc in ["top", "right"]:
        ax.spines[loc].set_visible(False)

    ax.grid(ls=":", alpha=0.5)
    ax.legend()
    ax.set_xlabel("chunk number")
    ax.set_ylabel("number of matches")

    fig.tight_layout()
    fn = os.path.join(d, f"number_of_catalog_matches_per_chunk.pdf")
    logger.debug(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()


def positional_outliers(
        base_name: str,
        wise_data: WISEDataBase
):
    """
    Plot the times of positional outliers (see :func:`get_positional_outliers_times`).
    """
    logger.info("plotting times of positional outliers")
    mjds_per_chunk = get_positional_outliers_times(base_name, wise_data)

    ic = 0.9

    data = np.array([
        [c] + list(np.quantile(mjds, [0.5, 0.5 - ic / 2, 0.5 + ic / 2]))
        for c, mjds in mjds_per_chunk.items()
    ])

    # -------- make plot --------- #

    fig, ax = plt.subplots()
    color = "r"
    lw = 2
    ax.plot(data[:, 0], data[:, 1], color=color, ls="-", label="median", lw=lw)
    ax.plot(data[:, 0], data[:, 2], color=color, ls="--", label="IC$_{" + f"{ic*100:.0f}" + "}%$", lw=lw)
    ax.plot(data[:, 0], data[:, 3], color=color, ls="--", lw=lw)
    ax.axhline(Time("2011-02-01").mjd, ls=":", label="WISE decommissioned")
    ax.axhline(Time("2013-09-01").mjd, ls=":", label="WISE reactivated")

    ax.set_xlabel("chunk number")
    ax.set_ylabel("MJD")
    ax.grid(ls=":", alpha=0.5)

    fig.tight_layout()
    fn = os.path.join(plots_dir("diagnostics", base_name), f"positional_outliers_times.pdf")
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()


def color_change(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        desc: str = "",
        xband: str = "W2",
):
    """
    Plot the change of magnitudes between the cataloged magnitudes and the magnitudes calculated from the measured
    baselines (see :func:`get_baseline_magnitudes`).

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: index of the database
    :type index: Index | None
    :param desc: description to be added to the file name
    :type desc: str
    :param xband: the band to use as the x-axis
    :type xband: str
    """
    diff = get_baseline_changes(base_name, database_name, wise_data, index=index)
    hist_kwargs = {"alpha": 0.5, "ec": "k"}
    _plots_dir = Path(plots_dir("diagnostics", base_name))

    # get the cataloged host magnitudes
    for band in ["W1", "W2"]:
        fig, ax = plt.subplots()
        ax.hist(diff[f"{band}_diff"], bins=100, **hist_kwargs)
        ax.set_xlabel(band + r"$_{\rm{measured}}$" + " - " + band + r"$_{\rm{catalog}}$")
        ax.set_ylabel("number of objects")
        ax.set_yscale("log")
        ax.axvline(0, ls=":", color="k", alpha=0.5)
        fn = _plots_dir / f"{desc}color_change_{band}.pdf"
        logger.info(f"saving under {fn}")
        fig.savefig(fn)
        plt.close()

    # plot the magnitude change in W1 vs W2
    fig, ax = plt.subplots()
    ax.scatter(diff["W1_diff"], diff["W2_diff"], s=1, alpha=0.01)
    ax.set_xlabel(r"W1$_{\rm{measured}}$ - W1$_{\rm{catalog}}$")
    ax.set_ylabel(r"W2$_{\rm{measured}}$ - W2$_{\rm{catalog}}$")
    ax.axhline(0, ls=":", color="k", alpha=0.5)
    ax.axvline(0, ls=":", color="k", alpha=0.5)
    ax.set_aspect("equal")
    fn = _plots_dir / f"{desc}color_change_W1_vs_W2.png"
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()

    # plot the color change
    fig, ax = plt.subplots()
    ax.hist(diff.color_change, bins=100, **hist_kwargs)
    ax.set_xlabel(r"(W1 - W2)$_{\rm{measured}}$ - (W1 - W2)$_{\rm{catalog}}$")
    ax.set_ylabel("number of objects")
    ax.set_yscale("log")
    ax.axvline(0, ls=":", color="k", alpha=0.5)
    fn = _plots_dir / f"{desc}color_change_W1_minus_W2.pdf"
    logger.info(f"saving under {fn}")
    fig.savefig(fn)

    # plot the color change vs w1 mag
    xkey = f"{xband}_catalog_mag"
    xlabel = xband + r"$_{\rm{catalog}}$"
    ykeys = ["W1_diff", "W2_diff", "color_change"]
    ylabels = [
        r"W1$_{\rm{measured}}$ - W1$_{\rm{catalog}}$",
        r"W2$_{\rm{measured}}$ - W2$_{\rm{catalog}}$",
        r"(W1 - W2)$_{\rm{measured}}$ - (W1 - W2)$_{\rm{catalog}}$"
    ]
    xbins = np.linspace(diff[xkey].min(), diff[xkey].max(), 100)
    xbin_mids = (xbins[1:] + xbins[:-1]) / 2
    grouped_diff = diff.groupby(pd.cut(diff[xkey], xbins))
    ncols = 1
    nrows = len(ykeys)
    figsize = plt.rcParams["figure.figsize"] * np.array([ncols, nrows])

    fig, axs = plt.subplots(sharex=True, figsize=figsize, nrows=nrows, ncols=ncols, gridspec_kw={"hspace": 0})
    for ax, ykey, ylabel in zip(axs, ykeys, ylabels):
        ax.scatter(diff[xkey], diff[ykey], s=1, alpha=0.01)
        qs = grouped_diff[ykey].quantile([0.16, 0.5, 0.84])
        ax.plot(xbin_mids, qs[:, 0.5], color="k", alpha=0.5)
        ax.plot(xbin_mids, qs[:, 0.16], color="k", ls="--", alpha=0.5)
        ax.plot(xbin_mids, qs[:, 0.84], color="k", ls="--", alpha=0.5)
        ax.axhline(0, ls=":", color="k")
        ax.set_ylabel(ylabel)

    # add the fit
    cg = {"W1": 15, "W2": 14.5}
    change_fit = get_baseline_change_fit(base_name, database_name, wise_data, index=index, xkey=xkey, cutoff_guess=cg)
    xfit = np.linspace(14, 20, 100)
    w1fit_model = cutoff_model(xfit, cutoff=change_fit["W1"]["cutoff"], slope=change_fit["W1"]["slope"])
    w2fit_model = cutoff_model(xfit, cutoff=change_fit["W2"]["cutoff"], slope=change_fit["W2"]["slope"])
    color_model = w1fit_model - w2fit_model
    for i, (ax, model) in enumerate(zip(axs, [w1fit_model, w2fit_model, color_model])):
        if i < 2:
            cutoff = change_fit[f"W{i + 1}"]["cutoff"]
            slope = change_fit[f"W{i + 1}"]["slope"]
            label = f"cutoff: {cutoff:.2f}, slope: {slope:.2f}"
        else:
            label = ""
        ax.plot(xfit, model, color="r", label=label)
        ax.legend()

    axs[-1].set_xlabel(xlabel)
    fn = _plots_dir / f"{desc}color_change_W1_minus_W2_vs_W1.png"
    logger.info(f"saving under {fn}")
    fig.savefig(fn)

    # plot new color vs old color
    fig, ax = plt.subplots()
    ax.scatter(diff["measured_color"], diff["catalog_color"], s=1, alpha=0.01)
    ax.set_xlabel(r"(W1 - W2)$_{\rm{measured}}$")
    ax.set_ylabel(r"(W1 - W2)$_{\rm{catalog}}$")
    ax.set_aspect("equal")
    xx = np.linspace(*ax.get_xlim(), 100)  # type: ignore
    ax.plot(xx, xx, ls=":", color="k")
    fn = _plots_dir / f"{desc}color_change_W1_minus_W2_vs_W1_minus_W2.png"
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()


def strength_vs_color(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        desc: str = ""
):
    """
    ..warning:: not tested

    Plot the strength of the candidates vs the color change.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: index of the candidates
    :type index: Index | None
    :param desc: description to be added to the file name
    :type desc: str
    """
    connector = DatabaseConnector(database_name=database_name, base_name=base_name)
    info = pd.concat([
        connector.get_strength(index),
        get_baseline_changes(base_name, database_name, wise_data, index=index)
    ], axis=1)

    logger.debug(info[["min_strength_by_var", "measured_color"]].describe(include="all"))

    fig, ax = plt.subplots()
    ax.scatter(info["measured_color"], info["min_strength_by_var"], s=1, alpha=0.01)
    ax.set_xlabel(r"(W1 - W2)$_{\rm{measured}}$")
    ax.set_ylabel("strength")
    ax.set_yscale("log")
    fn = os.path.join(plots_dir("diagnostics", base_name), f"{desc}strength_vs_color.png")
    logger.info(f"saving under {fn}")
    fig.savefig(fn)
    plt.close()


def plot_separation(
        base_name: str,
        database_name: str,
        wise_data: WiseDataByVisit,
        index: Index,
        mask_by_position: bool,
        service: str = "tap",
        arcsec: float = 6,
        loaded_data: pd.DataFrame = None,
        ax: plt.Axes | None = None,
        save: bool = True
):
    """
    Plot the separation of the flare position from the baseline position.

    :param base_name: base name of the analysis
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: index of the object
    :type index: Index
    :param mask_by_position: whether to mask the datapoints by position
    :type mask_by_position: bool
    :param service: the service to use, either "tap" or "gator", defaults to "tap"
    :type service: str, optional
    :param arcsec: the size of the cutout in arcsec, defaults to 6
    :type arcsec: float, optional
    :param loaded_data:
        the unbinned lightcurves from :func:`WISEData.get_unbinned_lightcurves()`,
        if not given, they will be loaded
    :type loaded_data: pd.DataFrame, optional
    :param ax: the axis to plot on, if not given, a new figure will be created
    :type ax: plt.Axes, optional
    :param save: whether to save the plot
    :type save: bool
    """
    logger.info(f"plotting separation for {index} of {base_name} and {database_name}")

    # load unbinned lightcurve if not given
    if loaded_data is None:
        chunk_number = wise_data._get_chunk_number(parent_sample_index=index)
        loaded_data = wise_data.get_unbinned_lightcurves(chunk_number=chunk_number)

    # select the datapoints belonging to this object
    loaded_data = loaded_data[loaded_data[wise_data._tap_orig_id_key] == index]
    logger.debug(f"selected {len(loaded_data)} data points")

    # select data by position if mask_by_position
    if mask_by_position:
        chunk_number = locals().get("chunk_number", wise_data._get_chunk_number(parent_sample_index=index))
        position_mask = wise_data.get_position_mask(chunk_number=chunk_number, service=service)
        if str(index) in position_mask:
            loaded_data = loaded_data[~loaded_data.index.isin(position_mask[str(index)])]
        # if there are no bad datapoints, we do not need to mask

    # calculate positions relative to the parent sample position
    separations = get_separation(base_name, database_name, wise_data, mask_by_position, index)
    ra_key = wise_data.parent_sample.default_keymap["ra"]
    dec_key = wise_data.parent_sample.default_keymap["dec"]
    pos = wise_data.parent_sample.df.loc[index, [ra_key, dec_key]]
    with pd.option_context('mode.chained_assignment', None):
        separations["rel_baseline_ra"] = (separations["baseline_ra"] - pos[ra_key]) * 3600
        separations["rel_baseline_dec"] = (separations["baseline_dec"] - pos[dec_key]) * 3600
        separations["rel_flare_ra"] = (separations["flare_ra"] - pos[ra_key]) * 3600
        separations["rel_flare_dec"] = (separations["flare_dec"] - pos[dec_key]) * 3600
        loaded_data["rel_ra"] = (loaded_data["ra"] - pos[ra_key]) * 3600
        loaded_data["rel_dec"] = (loaded_data["dec"] - pos[dec_key]) * 3600

    # select flare time range
    connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    flare_mjds = connector.get_excess_mjd(index=index)
    flare_mjds.set_index(flare_mjds.index.astype(int), inplace=True)
    flare_mjds["latest_start"] = flare_mjds[["W1_excess_start_mjd", "W2_excess_start_mjd"]].max(axis=1)
    flare_mjds["earliest_end"] = flare_mjds[["W1_excess_end_mjd", "W2_excess_end_mjd"]].min(axis=1)
    flare_mask = loaded_data.mjd.between(flare_mjds.loc[index, "latest_start"], flare_mjds.loc[index, "earliest_end"])

    # plot the separation
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = plt.gcf()
    wise_data.parent_sample.plot_cutout(ind=index, ax=ax, which="panstarrs", arcsec=arcsec, plot_color_image=True)
    ax.scatter(loaded_data[~flare_mask]["rel_ra"], loaded_data[~flare_mask]["rel_dec"],
               s=3, ec="k", marker="o", fc="w", lw=0.5, label="baseline", zorder=5)
    ax.scatter(separations["rel_baseline_ra"], separations["rel_baseline_dec"],
               s=50, ec="k", marker="X", fc="w", lw=1, zorder=10)
    ax.scatter(loaded_data[flare_mask]["rel_ra"], loaded_data[flare_mask]["rel_dec"],
               s=3, ec="r", marker="o", fc="w", lw=0.5, label="flare", zorder=5)
    ax.scatter(separations["rel_flare_ra"], separations["rel_flare_dec"],
               s=50, ec="r", marker="X", fc="w", lw=1, zorder=10)
    ax.set_aspect(1, adjustable="box")
    ax.scatter([], [], marker="x", color="r", label="parent sample position")
    ax.legend()

    if save:
        masked_str = "masked" if mask_by_position else "unmasked"
        fn = Path(plots_dir("diagnostics", base_name)) / f"{index}_separation_{masked_str}.pdf"
        fn.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"saving under {fn}")
        fig.savefig(fn, bbox_inches="tight")
        plt.close()

    return fig, ax
