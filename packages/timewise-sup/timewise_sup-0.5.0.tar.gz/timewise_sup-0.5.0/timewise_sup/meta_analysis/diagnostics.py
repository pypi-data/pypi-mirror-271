"""
This module contains functions for calculating diagnostics for the meta-analysis. The diagnostics are saved to files
in the ``timewise_sup_data`` directory. The diagnostics are:

* ``statuses_per_chunk.json``: the status of the objects in each chunk
* ``catalog_matches_per_chunk.json``: the number of catalog matches in each chunk
* ``positional_outlier_mjds``: the MJDs of the positional outliers in each chunk

The functions are:

* :func:`calculate_positional_outlier_times` calculates the MJDs of the positional outliers in a given chunk
* :func:`get_statuses_per_chunk` gets the statuses of the objects in each chunk
* :func:`get_catalog_matches_per_chunk` gets the number of catalog matches in each chunk
* :func:`get_positional_outliers_times` gets the MJDs of the positional outliers in each chunk
* :func:`get_database_summary` gets a summary of the documents in the database
* :func:`get_baseline_magnitudes` gets the measured baseline magnitudes for the W1 and W2 bands
* :func:`get_baseline_changes` gets the change of magnitudes between the cataloged and measured magnitudes
* :func:`cutoff_model` is a model describing a constant and linear model at a cutoff
* :func:`fit_baseline_changes` fits the change of magnitudes with the :func:`cutoff_model`
* :func:`get_baseline_change_fit` gets the fit of the change of magnitudes

"""

import logging
import os
import json
from pathlib import Path
import pandas as pd
import tqdm
from datetime import datetime
import numpy as np
from scipy.optimize import curve_fit
from timewise.wise_data_base import WISEDataBase

from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index
from timewise_sup.meta_analysis.catalog_match import get_catalog_match_mask


logger = logging.getLogger(__name__)


def get_statuses_per_chunk(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase
) -> dict:
    """
    Get the statuses of the objects in each chunk. The statuses are saved to a file in the ``timewise_sup_data``
    directory. If the file already exists, it is loaded from there. Otherwise, it is calculated and saved.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the statuses of the objects in each chunk
    :rtype: dict
    """
    logger.info(f"getting statuses per chunk for {base_name}")
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, "statuses_per_chunk.json")

    if not os.path.isfile(fn):
        logger.debug(f"No file {fn}. Calculating")
        chunks = list(range(wise_data.n_chunks))

        logger.info("getting statusees")
        statusees = dict()
        for c in chunks:
            m = wise_data.chunk_map == c
            ids = wise_data.parent_sample.df.index[m]
            status = DatabaseConnector(base_name=base_name, database_name=database_name).get_status(ids)
            statusees[c] = list(status.status)

        logger.debug(f"saving under {fn}")
        with open(fn, "w") as f:
            json.dump(statusees, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            statusees = json.load(f)

    return statusees


def get_catalog_matches_per_chunk(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase
) -> dict:
    """
    Get the number of catalog matches in each chunk. The number of catalog matches are saved to a file in the
    ``timewise_sup_data`` directory. If the file already exists, it is loaded from there. Otherwise, it is calculated
    and saved.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the number of catalog matches in each chunk
    :rtype: dict
    """
    logger.info("getting catalog matches per chunk")

    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, base_name, "catalog_matches_per_chunk.json")

    if not os.path.isfile(fn):
        logger.debug(f"No file {fn}. Calculating")

        chunks = list(range(wise_data.n_chunks))

        matches_per_chunk = dict()
        for c in chunks:
            m = wise_data.chunk_map == c
            ids = wise_data.parent_sample.df.index[m]
            chunk_match_mask = get_catalog_match_mask(base_name, database_name, ids)

            chunk_matches = dict()
            for catalogue_name in chunk_match_mask.columns:
                chunk_matches[catalogue_name] = int(chunk_match_mask[catalogue_name].sum())

            matches_per_chunk[c] = chunk_matches

        logger.debug(f"saving to {fn}")
        with open(fn, "w") as f:
            json.dump(matches_per_chunk, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            matches_per_chunk = json.load(f)

    return matches_per_chunk


def calculate_positional_outlier_times(
        wise_data: WISEDataBase,
        chunk_number: int
) -> list:
    """
    Use :class:`timewise` to calculate the MJDs of the positional outliers in a given chunk.
    See the `documentation
    <https://timewise.readthedocs.io/en/latest/api.html#timewise.wise_data_base.WISEDataBase.get_position_mask>`_
    for more information.

    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param chunk_number: the chunk number
    :type chunk_number: int
    :return: the MJDs of the positional outliers in the chunk
    :rtype: list
    """
    logging.getLogger("timewise").setLevel(logging.getLogger("timewise_sup").getEffectiveLevel())
    unbinned_lcs = wise_data.get_unbinned_lightcurves(chunk_number=chunk_number)
    position_masks = wise_data.get_position_mask(service="tap", chunk_number=chunk_number)

    mjds = list()

    for ind, position_mask in tqdm.tqdm(position_masks.items(), desc="going through lightcurves"):
        lc = unbinned_lcs[unbinned_lcs[wise_data._tap_orig_id_key] == int(ind)]
        mjds.extend(list(lc.loc[position_mask].mjd.values))

    return mjds


def get_positional_outliers_times(
        base_name,
        wise_data: WISEDataBase
) -> dict:
    """
    Get the MJDs of the positional outliers in each chunk. The MJDs are saved to files in the ``timewise_sup_data``
    directory. If the files already exist, they are loaded from there. Otherwise, they are calculated and saved.

    :param base_name: base name of the WISE data
    :type base_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :return: the MJDs of the positional outliers in each chunk
    :rtype: dict
    """
    logger.info(f"getting positional outlier times")

    tsup_data = load_environment("TIMEWISE_SUP_DATA")
    cache_dir = os.path.join(tsup_data, base_name, "positional_outlier_mjds")
    os.makedirs(cache_dir, exist_ok=True)

    mjds_per_chunk = dict()

    for c in tqdm.tqdm(range(wise_data.n_chunks), desc="going through chunks"):
        fn = os.path.join(cache_dir, f"{c}.json")

        if not os.path.isfile(fn):
            logger.debug(f"file {fn} not found. Calculating")
            mjds = calculate_positional_outlier_times(wise_data, c)
            logger.debug(f"saving to {fn}")

            with open(fn, "w") as f:
                json.dump(mjds, f)

        else:
            logger.debug(f"loading {fn}")
            with open(fn, "r") as f:
                mjds = json.load(f)

        mjds_per_chunk[c] = mjds

    return mjds_per_chunk


def get_database_summary(base_name: str, database_name: str) -> pd.DataFrame:
    """
    Get a summary of the documents in the database. Count documents of the following units:
    - ```T2CatalogMatch```
    - ```T2DigestRedshifts```
    - ```T2BayesianBlocks```
    - ```T2DustEchoEval```
    Count their numbers for each document code.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :return: dataframe with the summary
    :rtype: pd.DataFrame
    """
    logger.info(f"getting database summary for {base_name}")
    t2col = DatabaseConnector(base_name=base_name, database_name=database_name).t2collection
    codes = t2col.distinct("code")
    units = ["T2CatalogMatch", "T2DigestRedshifts", "T2BayesianBlocks", "T2DustEchoEval"]
    summary = pd.DataFrame(index=codes, columns=units)
    unit_codes = [(unit, code) for unit in units for code in codes]
    for unit, code in tqdm.tqdm(unit_codes, desc="going through units and codes"):
        summary.loc[code, unit] = t2col.count_documents({"unit": unit, "code": code})
    t = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fn = (
            Path(load_environment("TIMEWISE_SUP_DATA")) /
            base_name /
            database_name /
            f"database_summary_{t}.csv"
    )
    fn.parent.mkdir(parents=True, exist_ok=True)
    logger.debug(f"saving to {fn}")
    summary.to_csv(fn)
    return summary


def get_baseline_magnitudes(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index
):
    """
    Get the baseline magnitudes for the W1 and W2 bands as calculated from the measured baseline flux densities.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: index of the objects
    :type index: Index
    :return: dataframe with the baseline magnitudes
    :rtype: pd.DataFrame
    """

    connector = DatabaseConnector(database_name=database_name, base_name=base_name)

    baselines = connector.get_baselines(index=index)
    with np.errstate(invalid="ignore"):  # ignore negative values in log10, will give NaNs which is exactly what we want
        for b in ["W1", "W2"]:
            baselines[f"{b}_mag"] = (
                -2.5 * np.log10(baselines[f"{b}_baseline"] / wise_data.magnitude_zeropoints['F_nu'][b].to('mJy').value)
            )
            baselines[f"{b}_mag_err"] = (
                2.5 / np.log(10) * baselines[f"{b}_baseline_sigma"] / baselines[f"{b}_baseline"]
            )

    return baselines


def get_baseline_changes(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index
) -> pd.DataFrame:
    """
    Get the change of magnitudes between the cataloged magnitudes and the magnitudes calculated from the measured
    baselines (see :func:`get_baseline_magnitudes`). Also calculate the color and its change.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: index of the objects
    :type index: Index
    :return: dataframe with the changes of magnitudes
    :rtype: pd.DataFrame
    """
    parent_sample = wise_data.parent_sample
    wise_mag_keys = ["W1_mag", "W2_mag"]
    if any([b not in parent_sample.default_keymap for b in wise_mag_keys]):
        raise KeyError(
            f"Could not find the WISE magnitudes in the parent sample. "
            f"Make sure the parent sample has the keys {wise_mag_keys} in the `default_keymap`."
        )
    mag_keys = {b: parent_sample.default_keymap[b] for b in wise_mag_keys}
    logger.debug(f"WISE filter mag keys are {mag_keys}")
    catalog_magnitudes = parent_sample.df[[mag_keys["W1_mag"], mag_keys["W2_mag"]]]
    no_catalog_mags = catalog_magnitudes.isna().any(axis=1)
    catalog_magnitudes = catalog_magnitudes[~no_catalog_mags]
    catalog_magnitudes.set_index(catalog_magnitudes.index.astype(str), inplace=True)

    # get the magnitudes calculated fom the measured baselines
    measured_baselines = get_baseline_magnitudes(base_name, database_name, wise_data, index=index)
    upper_limits = measured_baselines["W1_mag"].isna() | measured_baselines["W2_mag"].isna()
    good_detection = (
            ((measured_baselines["W1_baseline"] / measured_baselines["W1_baseline_sigma"]) > 3) &
            ((measured_baselines["W2_baseline"] / measured_baselines["W2_baseline_sigma"]) > 3)
    )
    measured_baselines = measured_baselines[~upper_limits & good_detection]

    # find common indices
    common_index = measured_baselines.index.intersection(catalog_magnitudes.index)

    # plot the change of magnitudes
    columns = ["W1_measured_mag", "W2_measured_mag",
               "W1_catalog_mag",  "W2_catalog_mag",
               "W1_diff",         "W2_diff",
               "measured_color",  "catalog_color", "color_change"]
    diff = pd.DataFrame(columns=columns, index=common_index)
    for band in ["W1", "W2"]:
        diff[f"{band}_measured_mag"] = measured_baselines.loc[common_index, f"{band}_mag"]
        diff[f"{band}_catalog_mag"] = catalog_magnitudes.loc[common_index, mag_keys[f"{band}_mag"]]
        diff[f"{band}_diff"] = diff[f"{band}_measured_mag"] - diff[f"{band}_catalog_mag"]

    diff["measured_color"] = diff["W1_measured_mag"] - diff["W2_measured_mag"]
    diff["catalog_color"] = diff["W1_catalog_mag"] - diff["W2_catalog_mag"]
    diff["color_change"] = diff["measured_color"] - diff["catalog_color"]

    return diff


def cutoff_model(x: np.ndarray, cutoff: float, slope: float, constant: float = 0) -> np.ndarray:
    """
    A model for the cutoff of the linear model.

    :param x: the x values
    :type x: np.ndarray
    :param cutoff: the cutoff value
    :type cutoff: float
    :param slope: the slope of the linear model
    :type slope: float
    :param constant: the constant of the linear model
    :type constant: float
    :return: the model values
    :rtype: np.ndarray
    """
    return np.where(x > cutoff, slope * (x - cutoff) + constant, constant)


def fit_baseline_changes(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        cutoff_guess: dict[str, float],
        mag_range: tuple[float, float] = (14, 20),
        xkey: str = "W1_catalog_mag"
) -> dict[str, dict[str, float]]:
    """
    Fit the changes of magnitudes between the cataloged magnitudes and the magnitudes calculated from the measured
    baselines as a function of the cataloged W1 mag (see :func:`get_baseline_changes`) with a combination of a constant
    and linear model to get the sensitivity of the WISE bands.

    :param base_name: base name of the wise data
    :type base_name: str
    :param database_name: name of the database
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: index of the objects
    :type index: Index
    :param mag_range: the range of magnitudes to fit
    :type mag_range: tuple[float, float]
    :param cutoff_guess: the guess for the cutoff of the linear model
    :type cutoff_guess: dict[str, float] | None
    :param xkey: the key of the x values
    :type xkey: str
    """
    logger.info(f"fitting baseline changes for {base_name}")

    diff = get_baseline_changes(base_name, database_name, wise_data, index)
    fit = dict()
    for band in ["W1", "W2"]:
        logger.info(f"fitting {band} band")
        band_mag_mask = (diff[xkey] > mag_range[0]) & (diff[xkey] < mag_range[1])
        diff_band = diff[band_mag_mask]

        xbins = np.linspace(diff_band[xkey].min(), diff_band[xkey].max(), 50)
        xbin_mids = (xbins[1:] + xbins[:-1]) / 2
        med = diff_band.groupby(pd.cut(diff[xkey], xbins))[f"{band}_diff"].median()
        std = diff_band.groupby(pd.cut(diff[xkey], xbins))[f"{band}_diff"].std()
        notna_mask = ~np.isnan(med) & ~np.isnan(std)
        x = xbin_mids[notna_mask]
        y = med[notna_mask]
        yerr = std[notna_mask]
        logger.debug(f"fitting {band} band with {len(x)} points")
        logger.debug("\n" + pd.DataFrame({"x": x, "y": y, "yerr": yerr}).to_string())

        p0 = [cutoff_guess[band], -1]
        logger.debug(f"initial guess: {p0}")
        popt, pcov = curve_fit(cutoff_model, x, y, p0=p0, sigma=yerr, absolute_sigma=True)
        perr = np.sqrt(np.diag(pcov))
        logger.debug(f"fit result: {popt}")
        logger.debug(f"fit errors: {perr}")

        fit[band] = {
            "cutoff": popt[0],
            "cutoff_err": perr[0],
            "slope": popt[1],
            "slope_err": perr[1],
        }

    return fit


def get_baseline_change_fit(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        mag_range: tuple[float, float] = (14, 20),
        cutoff_guess: dict[str, float] | None = None,
        xkey: str = "W1_catalog_mag"
):
    """
    Get the fit of the changes of magnitudes between the cataloged magnitudes and the magnitudes calculated from the
    measured baselines (see :func:`fit_baseline_changes`). The fit is saved to a file in the ``timewise_sup_data``
    directory based on a hash of the input parameters. If the file already exists, it is loaded from there. Otherwise,
    it is calculated and saved.
    """
    logger.info(f"getting baseline change fit for {base_name}")
    if cutoff_guess is None:
        cutoff_guess = {"W1": 15, "W2": 15}
    tsup_data = Path(load_environment("TIMEWISE_SUP_DATA"))
    cache_dir = tsup_data / base_name / database_name / "baseline_change_fit"
    cache_dir.mkdir(parents=True, exist_ok=True)

    _cutoff_hashable = tuple(sorted(list(cutoff_guess.items())))
    _index_hashable = tuple(sorted(list(np.atleast_1d(index))))
    input_hash = hash((base_name, database_name, wise_data, _index_hashable, mag_range, _cutoff_hashable, xkey))
    fn = cache_dir / f"{input_hash}.json"

    if not os.path.isfile(fn):
        logger.debug(f"file {fn} not found. Calculating")
        fit = fit_baseline_changes(
            base_name=base_name,
            database_name=database_name,
            wise_data=wise_data,
            index=index,
            cutoff_guess=cutoff_guess,
            mag_range=mag_range,
            xkey=xkey
        )
        logger.debug(f"saving to {fn}")
        with open(fn, "w") as f:
            json.dump(fit, f)

    else:
        logger.debug(f"loading {fn}")
        with open(fn, "r") as f:
            fit = json.load(f)

    return fit
