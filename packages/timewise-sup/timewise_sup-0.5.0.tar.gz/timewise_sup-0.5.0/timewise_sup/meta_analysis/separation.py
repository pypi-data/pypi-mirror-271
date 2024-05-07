"""
Calculate the separation between the flare and the baseline position of the objects in the database.

* :func:`mean_position` calculates the mean position of a set of coordinates.
* :func:`calculate_separation` calculates the separation for a given set of objects.
* :func:`get_separation` retrieves the separation from the cache or calculates it if necessary.
"""


import logging
from pathlib import Path
import pandas as pd
from typing import Sequence
from astropy.coordinates.angle_utilities import angular_separation
from scipy.optimize import minimize
import numpy as np

from timewise.wise_data_base import WISEDataBase
from timewise_sup.environment import load_environment
from timewise_sup.mongo import DatabaseConnector, Index


logger = logging.getLogger(__name__)


def mean_position(ra: Sequence[float], dec: Sequence[float], minimize_options: dict | None = None) -> tuple[float, float]:
    """
    Calculate the mean position of a set of coordinates by minimising the sum of squared angular distances.

    :param ra: Right ascension in radians
    :type ra: Sequence[float]
    :param dec: Declination in radians
    :type dec: Sequence[float]
    :param minimize_options: Options for the minimization, passed to :func:`scipy.optimize.minimize`
    :type minimize_options: dict, optional
    :return: Mean right ascension and declination in radians
    :rtype: tuple[float, float]
    """

    def sum_of_squared_angular_distance(x):
        return sum(angular_separation(ra, dec, *x) ** 2)

    _minimize_options = minimize_options or {}
    result = minimize(
        sum_of_squared_angular_distance,
        x0=(np.median(ra), np.median(dec)),
        bounds=[(0, 2 * np.pi), (-np.pi / 2, np.pi / 2)],
        jac=_minimize_options.pop("jac", None),
        options=_minimize_options
    )

    if not result.success:
        raise ValueError(f"Optimization failed: {result.message}")

    return result.x


def calculate_separation(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        index: Index,
        mask_by_position: bool,
        service: str = "tap",
        minimize_options: dict | None = None
) -> pd.DataFrame:
    """
    Calculate the separation for a given set of objects.

    :param base_name: the base name of the WISE data
    :type base_name: str
    :param database_name: the database name
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param index: the index of the objects
    :type index: Index
    :param mask_by_position: whether to mask by position
    :type mask_by_position: bool
    :param service: the service to use, either of "tap" or "gator"
    :type service: str
    :param minimize_options: Options for the minimization, passed to :func:`scipy.optimize.minimize`
    :type minimize_options: dict, optional
    :return: the separation
    :rtype: pd.DataFrame
    """
    index1d = np.atleast_1d(index)
    logger.info(f"Calculating separation for {len(index1d)} objects of {base_name} and {database_name}")

    # get the flare times to select corresponding datapoints
    connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    flare_mjds = connector.get_excess_mjd(index=index1d)  # type: ignore
    flare_mjds.set_index(flare_mjds.index.astype(int), inplace=True)
    flare_mjds["latest_start"] = flare_mjds[["W1_excess_start_mjd", "W2_excess_start_mjd"]].max(axis=1)
    flare_mjds["earliest_end"] = flare_mjds[["W1_excess_end_mjd", "W2_excess_end_mjd"]].min(axis=1)

    # set up empty result dataframe
    columns = [
        "baseline_ra",
        "baseline_dec",
        "flare_ra",
        "flare_dec",
        "flare_separation_data",
        "flare_separation_parent_sample",
        "baseline_separation_parent_sample"
    ]
    separation = pd.DataFrame(index=index1d, columns=columns, dtype=float)

    # find the chunks to load
    chunk_numbers = pd.Series([wise_data._get_chunk_number(parent_sample_index=i) for i in index1d], index=index1d)
    unique_chunks = chunk_numbers.unique()
    logger.debug(f"loading {len(unique_chunks)} chunks")

    # load the parent sample to be able to calculate the separation to the parent sample position
    parent_sample = wise_data.parent_sample
    ra_key = parent_sample.default_keymap["ra"]
    dec_key = parent_sample.default_keymap["dec"]
    parent_sample_positions = (
        parent_sample
        .df[[ra_key, dec_key]]
        .loc[index1d]
        .rename(columns={ra_key: "ra", dec_key: "dec"})
        * np.pi / 180
    )

    # load the unbinned lightcurves and calculate the separation
    # because the data is saved per chunk, it is more efficient to load the data chunk by chunk
    for c in unique_chunks:
        unbinned_lightcurves = wise_data.get_unbinned_lightcurves(chunk_number=c)

        # if the data was binned while using positional masking, we need to repeat this here to get the
        # data that was actually used
        position_mask = wise_data.get_position_mask(chunk_number=c, service=service) if mask_by_position else None

        # calculate the separation for each object in the chunk
        for i in chunk_numbers[chunk_numbers == c].index:

            # select the data for the object
            unbinned_data = unbinned_lightcurves[unbinned_lightcurves[wise_data._tap_orig_id_key] == i]

            # if no position mask is given it means that there were no bad datapoints
            if mask_by_position and (str(i) in position_mask):
                ipm_list = position_mask[str(i)]
                logger.debug(f"masking {len(ipm_list)} datapoints of type {type(ipm_list[0])} for object {i}")
                logger.debug(f"lightcurve index is type {unbinned_data.index.dtype}")
                ipm = unbinned_data.index.isin(ipm_list)
                logger.debug(f"mask has length {ipm.sum()}")
                unbinned_data = unbinned_data[~ipm]

            # select the flare data
            flare_mask = unbinned_data.mjd.between(flare_mjds.loc[i, "latest_start"], flare_mjds.loc[i, "earliest_end"])

            # calculate the separation
            with pd.option_context('mode.chained_assignment', None):
                unbinned_data["ra_rad"] = np.radians(unbinned_data.ra)
                unbinned_data["dec_rad"] = np.radians(unbinned_data.dec)
            flare_position_rad = mean_position(
                unbinned_data[flare_mask].ra_rad,
                unbinned_data[flare_mask].dec_rad,
                minimize_options=minimize_options
            )
            baseline_position_rad = mean_position(
                unbinned_data[~flare_mask].ra_rad,
                unbinned_data[~flare_mask].dec_rad,
                minimize_options=minimize_options
            )
            flare_separation_data_rad = angular_separation(
                flare_position_rad[0],
                flare_position_rad[1],
                baseline_position_rad[0],
                baseline_position_rad[1]
            )
            flare_separation_parent_sample_rad = angular_separation(
                flare_position_rad[0],
                flare_position_rad[1],
                parent_sample_positions.loc[i, "ra"],
                parent_sample_positions.loc[i, "dec"]
            )
            baseline_separation_parent_sample_rad = angular_separation(
                baseline_position_rad[0],
                baseline_position_rad[1],
                parent_sample_positions.loc[i, "ra"],
                parent_sample_positions.loc[i, "dec"]
            )

            separation.loc[i] = [np.degrees(x) for x in [
                baseline_position_rad[0],
                baseline_position_rad[1],
                flare_position_rad[0],
                flare_position_rad[1],
                flare_separation_data_rad,
                flare_separation_parent_sample_rad,
                baseline_separation_parent_sample_rad
            ]]

    return separation


def get_separation(
        base_name: str,
        database_name: str,
        wise_data: WISEDataBase,
        mask_by_position: bool,
        index: Index | None = None,
        minimize_options: dict | None = None
) -> pd.DataFrame:
    """
    Get the separation from the cache or calculate it if necessary. See :func:`calculate_separation` for details.

    :param base_name: the base name of the WISE data
    :type base_name: str
    :param database_name: the database name
    :type database_name: str
    :param wise_data: the WISE data
    :type wise_data: WISEDataBase
    :param mask_by_position: whether to mask by position
    :type mask_by_position: bool
    :param index: the index of the objects, if not given, all dust-echo like objects are used, i.e. status "1"
    :type index: Index, optional
    :param minimize_options: Options for the minimization, passed to :func:`scipy.optimize.minimize`
    :type minimize_options: dict, optional
    :return: the separation
    :rtype: pd.DataFrame
    """
    logger.info(f"Getting separation for {base_name} ({database_name})")

    # set up cache file
    masked_str = "masked" if mask_by_position else "unmasked"
    cache_file = Path(load_environment("TIMEWISE_SUP_DATA")) / base_name / database_name / f"sep_{masked_str}.csv"

    # get the index
    connector = DatabaseConnector(base_name=base_name, database_name=database_name)
    _index = pd.Index(np.atleast_1d(index if index is not None else connector.get_ids("1")))
    logger.info(f"selected {len(_index)} objects")

    # calculate separation if not cache file exists
    if not cache_file.exists():
        logger.debug(f"Cache not found: {cache_file}")
        separation = calculate_separation(
            base_name,
            database_name,
            wise_data,
            _index,
            mask_by_position,
            minimize_options=minimize_options
        )
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Saving separation to cache: {cache_file}")
        separation.to_csv(cache_file)

    # load separation from cache
    else:
        logger.debug(f"Loading separation from cache: {cache_file}")
        separation = pd.read_csv(cache_file, index_col=0)

        # check if all objects are in the cache and calculate missing separations
        calculate_mask = ~_index.isin(separation.index)
        if calculate_mask.any():
            logger.debug(f"calculating separation for {sum(calculate_mask)} objects")
            missing_separation = calculate_separation(
                base_name,
                database_name,
                wise_data,
                _index[calculate_mask],
                mask_by_position,
                minimize_options=minimize_options
            )
            separation = pd.concat([separation, missing_separation])
            separation.to_csv(cache_file)

    return separation[separation.index.isin(_index)]
