"""
Module to interface with the :class:`MongoDB` database.

* :class:`DatabaseConnector`:
    The main class to interface with the database. It is initialized with the :attr:`base_name` and
    :attr:`database_name` and provides methods to get data from the database that was produced by :code:`AMPEL`.
"""

import logging
import os
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from pymongo import MongoClient, collection, database, errors as pymongo_errors
from collections.abc import Sequence
from pydantic import BaseModel
from pathlib import Path

from timewise_sup.environment import load_environment


logger = logging.getLogger(__name__)


jd_offset = -2400000.5


################################################################################
# -----------------------         utilities            ----------------------- #
# --------------------------------  START  ----------------------------------- #
#


Index = Sequence[str | int] | str | int
Status = str | Sequence[str]


def as_list(
        index: Index
) -> list:
    """
    Creates a list from input and transforms np.int64 to int

    :param index: objects to transform to list
    :type index: Index
    :return: the list
    :rtype: list
    """
    indices = list(np.atleast_1d(index))

    for i, ii in enumerate(indices):
        if isinstance(ii, np.int64):
            indices[i] = int(ii)

    return indices


def chunks(
        the_list: Sequence,
        length: int
):
    """
    Yield sequential chunks from l with fixed length

    :param the_list: sequence to be split into chunks
    :type the_list: Sequence
    :param length: length of isngle chunk
    :type length: int
    :return: generator creating the chunks
    :rtype: generator
    """
    number_of_chunks = int(np.ceil(len(the_list) / length))
    logger.debug(f"splitting {len(the_list)} into {number_of_chunks} chunks of length {length}")
    d, r = divmod(len(the_list), number_of_chunks)
    for i in range(number_of_chunks):
        logger.debug(f"chunk {i}")
        si = (d+1)*(i if i < r else r) + d*(0 if i < r else i - r)
        yield the_list[si:si+(d+1 if i < r else d)]


#
# -----------------------         utilities            ----------------------- #
# --------------------------------   END   ----------------------------------- #
################################################################################


################################################################################
# -----------------------      DatabaseConnector       ----------------------- #
# --------------------------------  START  ----------------------------------- #
#


class DatabaseConnector(BaseModel):
    """
    Class to connect to `MongoDB`

    :param base_name: The name given to the :class:`WISEData`
    :type base_name: str
    :param database_name: The name of the database in the :class:`MongoDB`
    :type database_name: str
    :param database: The database object from :class:`pymongo`
    :type database: :class:`pymongo.database.Database`
    :param t2collection: The collection object representing the tier 2 collection as used by :class:`AMPEL`
    :type t2collection: :class:`pymongo.collection.Collection`
    """

    base_name: str
    database_name: str
    database: database.Database
    t2collection: collection.Collection

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **kwargs):
        # get the client, database and t2 collections
        client: MongoClient = DatabaseConnector.connect_to_db()
        _database_name = kwargs["database_name"]

        if _database_name not in client.list_database_names():
            logger.warning(f"No database with name {_database_name} registered in client!")

        _database = client[_database_name]
        kwargs["database"] = _database
        kwargs["t2collection"] = _database["t2"]

        super().__init__(**kwargs)

    @property
    def cache_dir(self) -> Path:
        """Directory used to store cache"""
        tsup_data = Path(load_environment("TIMEWISE_SUP_DATA"))
        return tsup_data / self.base_name / self.database_name

    ################################################################################
    # -----------------------  interface with MongoDB      ----------------------- #
    # --------------------------------  START  ----------------------------------- #
    #

    @staticmethod
    def connect_to_db() -> MongoClient:
        """Return the :class:`MongoClient`"""
        mongodb_port = load_environment("TIMEWISE_SUP_MONGODB_PORT")
        logger.debug(f"connecting to MongoDB at {mongodb_port}")
        client: MongoClient = MongoClient(f"mongodb://localhost:{mongodb_port}/")
        try:
            # The ping command is cheap and does not require auth.
            client.admin.command('ping')
        except pymongo_errors.ConnectionFailure as e:
            raise pymongo_errors.ConnectionFailure(f"Could not connect to MongoDB at {mongodb_port}!") from e
        logger.debug("connected")
        return client

    def get_dataframe(
            self,
            collection_name: str,
            field_name_lists: list[list[str | int]],
            filter: dict | None = None
    ) -> pd.DataFrame:
        """
        Get fields from a collection in the database and return as :class:`pandas.DataFrame`.

        :param collection_name: Name of the collection
        :type collection_name: str
        :param field_name_lists: The "path" to the value in the collection
        :type field_name_lists: list of lists
        :param filter: filter to apply to the entries
        :type filter: dict
        :return: the selected data
        :rtype: pandas.DataFrame
        """
        logger.info(f"making dataframe from {field_name_lists} of {self.database_name}.{collection_name}")
        col = self.database[collection_name]  # type: collection.Collection
        filter = dict() if filter is None else filter

        res: dict[str, list] = {f"field{i}": list() for i in range(len(field_name_lists))}
        for entry in col.find(filter):
            for i_field_names, field_names in enumerate(field_name_lists):

                # loop through the list of field names / indices to dig down to the value
                val = entry
                for field_name in field_names:
                    if field_name not in val:
                        val = np.nan
                        break
                    val = val[field_name]

                res[f"field{i_field_names}"].append(val)

        return pd.DataFrame.from_dict(res)

    def drop_stocks(self, stocks: Index, tiers: list[int] | None = None):
        """Drop lightcurves and related results from the database"""
        indices = as_list(stocks)
        _tiers = [0, 1, 2] if tiers is None else tiers
        logger.debug(f"dropping {len(indices)} indices of {self.base_name} from {self.database_name} (tiers {_tiers})")

        f = {"stock": {"$in": indices}}

        if 0 in _tiers:
            t0 = self.database["t0"]
            logger.info("dropping datapoints")
            for index in tqdm(indices, desc="dropping datapoints"):
                t0.delete_many({"stock": int(index)})

        if 1 in _tiers:
            t1 = self.database["t1"]
            logger.info("dropping lightcurves")
            t1.delete_many(f)

        if 2 in _tiers:
            logger.info("dropping T2 results")
            self.t2collection.delete_many(f)

    #
    # -----------------------  interface with MongoDB      ----------------------- #
    # --------------------------------   END   ----------------------------------- #
    ################################################################################

    ################################################################################
    # ------------------     get T2DustEchoEval results       -------------------- #
    # --------------------------------  START  ----------------------------------- #
    #

    def get_status(
            self,
            index: Index
    ) -> pd.DataFrame:
        """
        Get the status of objects as determined by the pipline.

        :param index: The index of the objects in the :class:`timewise.ParentSample`
        :type index: Index
        :return: Status of the objects
        :type: pandas.DataFrame
        """
        indices = as_list(index)
        logger.debug(f"getting status for {len(indices)} IDs ({self.base_name} in {self.database_name})")

        columns = {
            "stock": 1,
            "body.status": 1
        }

        i = None
        status = dict()
        for chunked_indices in chunks(indices, int(1e6)):
            dust_echo_filter = {
                "unit": "T2DustEchoEval",
                "code": 0,
                "stock": {"$in": chunked_indices}
            }
            for i, x in enumerate(self.t2collection.find(dust_echo_filter, columns)):
                status[str(x["stock"])] = {"status": x['body'][-1]['status']}

        if len(status) == 0:
            return pd.DataFrame({"status": []})

        return pd.DataFrame.from_dict(status, orient="index")

    def get_unique_statuses(self) -> list:
        """Returns a :class:`list` of all unique statuses"""
        filter = {
            "unit": "T2DustEchoEval",
            "code": 0
        }
        statuses = self.t2collection.distinct("body.status", filter)
        return statuses

    def _calculate_ids(self, status: str) -> list:
        """
        Finds the IDs for a status

        :param status: The status for which the IDs should be calculated for
        :type status: str
        :return: The IDs
        :rtype: list
        """
        logger.debug(f"calculating all IDs for status {status} ({self.base_name} in {self.database_name})")

        filter = {
            "unit": "T2DustEchoEval",
            "body.status": status,
            "code": 0
        }

        columns = {"stock": 1, "body.status": 1}
        stocks = list()
        n_wrong = 0
        for i in tqdm(self.t2collection.find(filter, columns), desc=f"getting IDs for status {status}"):
            stock = i["stock"]
            if i["body"][-1]["status"] != status:
                n_wrong += 1
            else:
                stocks.append(stock)

        stocks = as_list(np.unique(stocks))
        logger.debug(f"found {len(stocks)} stocks, {n_wrong} had matching status from previous run.")
        return stocks

    def get_ids(self, status: Status) -> list:
        """
        Get the IDs for a status. When called for the first time, caches the results to a file
        that will be loaded subsequently.

        :param status: The status
        :type status: Status
        :return: The IDs
        :rtype: list
        """
        logger.debug(f"getting all IDs for status {status} ({self.base_name} in {self.database_name})")

        ids_cache_dir = self.cache_dir / "ids"
        ids_cache_dir.mkdir(parents=True, exist_ok=True)

        stocks = list()

        for istatus in np.unique(status).astype(str):
            fn = ids_cache_dir / f"status{istatus.replace(' ', '_')}.json"

            if not os.path.isfile(fn):
                istocks = self._calculate_ids(istatus)
                logger.debug(f"caching to {fn}")
                with open(fn, "w") as f:
                    json.dump(istocks, f)

            else:
                logger.debug(f"loading cache from {fn}")
                with open(fn, "r") as f:
                    istocks = json.load(f)

                logger.debug(f"got {len(istocks)} ids")

            stocks.extend(istocks)

        return stocks

    def get_rejected_ids(self):
        """
        Get the ids of the rejected objects. The rejection reason is given in the description of the
        ``AMPEL`` ``T2DustEchoEval`` unit output.

        :return: ids of the rejected objects
        :rtype: list
        """
        logger.debug(f"getting rejected ids")
        rejected = (
            "No further investigation",
            "1_maybe_interesting",
            "2_maybe_interesting",
            "3", "3_maybe_interesting",
            "4", "4_maybe_interesting"
        )
        return self.get_ids(rejected)

    def get_excess_mjd(self, index: Index) -> pd.DataFrame:
        """
        Get the excess time for the given index

        :param index: The wanted index
        :type index: Index
        :return: Modified Julian Days of the excess, per filter, start, end and if flare ended
        :rtype: dict
        """
        indices = as_list(index)
        logger.debug(f"getting excess time for {len(indices)} IDs ({self.base_name} in {self.database_name})")

        excess_mjds = dict()

        for chunked_indices in chunks(indices, int(1e6)):
            bayesian_blocks_filter = {
                "unit": "T2BayesianBlocks",
                "stock": {"$in": chunked_indices},
                "code": 0
            }

            for i, x in enumerate(self.t2collection.find(bayesian_blocks_filter)):
                i_excess_mjds = dict()
                for f in ["W1", "W2"]:
                    excess_mags = np.array(x["body"][-1][f"Wise_{f}"]["max_mag_excess_region"])
                    excess_jds = x["body"][-1][f"Wise_{f}"]["jd_excess_regions"]
                    max_excess_mjds = np.array(excess_jds)[np.argmax(excess_mags)] + jd_offset

                    baseline_mjds = np.array(x["body"][-1][f"Wise_{f}"]["jd_baseline_regions"]).flatten() + jd_offset
                    excess_ended = max(baseline_mjds) > max(max_excess_mjds)

                    i_excess_mjds[f"{f}_excess_start_mjd"] = min(max_excess_mjds)
                    i_excess_mjds[f"{f}_excess_end_mjd"] = max(max_excess_mjds)
                    i_excess_mjds[f"{f}_flare_ended"] = excess_ended

                excess_mjds[str(x["stock"])] = i_excess_mjds

        return pd.DataFrame.from_dict(excess_mjds, orient="index")

    def _calculate_baselines(self, index: Index) -> pd.DataFrame:
        """
        Returns the baseline for the lightcurves.

        :param index: The index of the lightcurves
        :type index: Index
        :returns: The value of the baseline flux and the :math:`1\sigma` uncertainty per filter
        :rtype: dict
        """
        indices = as_list(index)
        logger.debug(f"reading baseline values for {len(indices)} objects")

        columns = ["W1_baseline", "W1_baseline_sigma", "W2_baseline", "W2_baseline_sigma"]
        baseline = pd.DataFrame(columns=columns, index=pd.Index(indices).astype(str))

        for chunked_indices in chunks(indices, int(5e5)):

            dust_echo_filter = {
                "unit": "T2DustEchoEval",
                "stock": {"$in": chunked_indices},
                "code": 0
            }

            for x in self.t2collection.find(
                    dust_echo_filter,
                    {"stock": 1}
            ):
                stock = x["stock"]
                stock_str = str(stock)
                for y in self.t2collection.find(
                        {"unit": "T2BayesianBlocks", "stock": stock, "code": 0},
                        {f"body.Wise_{b}.baseline{s}": 1 for b in ["W1", "W2"] for s in ["", "_sigma"]},
                        limit=1
                ):
                    for b in ["W1", "W2"]:
                        baseline.loc[stock_str, f"{b}_baseline"] = y["body"][-1][f"Wise_{b}"]["baseline"]
                        baseline.loc[stock_str, f"{b}_baseline_sigma"] = y["body"][-1][f"Wise_{b}"]["baseline_sigma"]

        return baseline

    def get_baselines(self, index: Index) -> pd.DataFrame:
        """
        Returns the baseline for the lightcurves. Caches result to file when first called.

        :param index: The index of the lightcurves
        :type index: Index
        :returns: The value of the baseline flux and the :math:`1\sigma` uncertainty per filter
        :rtype: dict
        """
        fn = self.cache_dir / "baselines.csv"

        if not os.path.isfile(fn):
            logger.debug(f"no file {fn}")
            baseline = self._calculate_baselines(index)
            logger.debug(f"saving to {fn}")
            fn.parent.mkdir(parents=True, exist_ok=True)
            baseline.to_csv(fn)

        else:
            logger.debug(f"loading {fn}")
            baseline = pd.read_csv(fn, index_col=0)
            baseline.set_index(baseline.index.astype(str), inplace=True)

        indices = pd.Index(index).astype(str)
        indices_present = indices.isin(baseline.index)
        if np.any(~indices_present):
            logger.debug(f"{np.sum(~indices_present)} indices not found. calculating")
            baseline_suplement = self._calculate_baselines(indices[~indices_present].astype(int))
            baseline = pd.concat([baseline, baseline_suplement])
            logger.debug(f"saving {len(baseline)} baselines to {fn}")
            baseline.to_csv(fn)

        return baseline.loc[indices]

    def _calculate_t2_dust_echo_eval_descriptions(self, index: Index) -> pd.DataFrame:
        """
        Get the description for the lightcurves

        :param index: The index of the lightcurves
        :type index: Index
        :return: Description per lightcurves, separated by ", "
        :rtype: dict
        """
        indices = as_list(index)
        logger.debug(f"getting description for {len(indices)} objects of {self.base_name} in {self.database_name}")

        values = dict()

        for chunked_indices in chunks(indices, int(5e5)):
            filter = {
                "code": 0,
                "unit": "T2DustEchoEval",
                "stock": {"$in": chunked_indices}
            }

            for lc in self.t2collection.find(filter):
                value = dict()

                try:
                    value[f"description"] = ", ".join(lc["body"][-1]["description"])
                except KeyError as e:
                    raise KeyError(f"{lc}: {e}")

                values[str(lc["stock"])] = value

        logger.debug(f"returning {len(values)} results")

        return pd.DataFrame.from_dict(values, orient="index")

    def get_t2_dust_echo_eval_descriptions(self, indices: Index) -> pd.DataFrame:
        """
        Get the description of the lightcurves. Caches result to file when first called.

        :param indices: The index of the lightcurves
        :type indices: Index
        :return: Description per lightcurves, separated by ", "
        :rtype: dict
        """
        fn = self.cache_dir / "T2DustEchoEvalDescriptions.csv"
        fn.parents[0].mkdir(parents=True, exist_ok=True)

        if not os.path.isfile(fn):
            logger.debug(f"no file {fn}")
            desc = self._calculate_t2_dust_echo_eval_descriptions(indices)
            logger.debug(f"saving to {fn}")
            desc.to_csv(fn)

        else:
            logger.debug(f"loading {fn}")
            desc = pd.read_csv(fn, index_col=0)

        indices_series = pd.Series(indices)
        indices_present = indices_series.astype(str).isin(desc.index.astype(str))
        if np.any(~indices_present):
            logger.debug(f"{np.sum(~indices_present)} indices not found. calculating")
            desc_suplement = self._calculate_t2_dust_echo_eval_descriptions(indices_series[~indices_present])
            desc = pd.concat([desc, desc_suplement])
            logger.debug(f"saving {len(desc)} descriptions to {fn}")
            desc.to_csv(fn)

        return desc.loc[indices_series.astype(type(desc.index[0]))]

    def get_agn_variability_stocks(self) -> list:
        logger.debug("getting AGN stock IDs based on variability")

        filter = {
            '$and': [
                {"code": 0},
                {"unit": "T2DustEchoEval"},
                # {"body": {"$elemMatch": {"description": "Excess region exists"}}},
                {"body.description": {"$elemMatch": {"$ne": "Baseline only"}}},
                {"body.description": {"$elemMatch": {"$ne": "Stage transition"}}},
                {"body.status": {"$ne": "1"}}
                ]
        }

        cols = {"stock": 1}

        stocks = list()
        for lc in self.t2collection.find(filter, cols):
            stocks.append(lc["stock"])

        logger.debug(f"returning {len(stocks)} stock IDs")
        return stocks

    def get_strength(self, index: Index | str) -> pd.DataFrame:
        """
        Get the strength of the dust echo and the significance of the pre-flare variability per band

        :param index: The index of the lightcurves or "all"
        :type index: Index | str
        :return: The strength and significance per band
        :rtype: pandas.DataFrame
        """
        logger.info("getting strength")

        # load previous results if exist
        columns = [
            "W1_strength", "W1_pre_flare_var_sig", "W1_strength_by_var",
            "W2_strength", "W2_pre_flare_var_sig", "W2_strength_by_var",
            "min_strength", "max_var", "min_strength_by_var"
        ]

        use_all_indices = (isinstance(index, str) and (index == "all"))

        filename = self.cache_dir / "strength.json"
        if filename.is_file():
            logger.debug(f"loading strength from {filename}")
            strengths = pd.read_json(filename)
            strengths.set_index(strengths.index.astype(str), inplace=True)
        else:
            logger.debug(f"{filename} not found, creating empty DataFrame")
            strengths = pd.DataFrame(columns=columns)

        # set up query filter
        mongo_filter = {
            "unit": "T2BayesianBlocks",
            "code": 0
        }

        # if indices are specified, check if strengths are missing
        if not use_all_indices:
            _index = pd.Index(index).astype(str)
            missing_mask = ~_index.isin(strengths.index.astype(str))
            if missing_mask.any():
                logger.debug(f"found {missing_mask.sum()} missing strengths")
                strengths = pd.concat([strengths, pd.DataFrame(index=_index[missing_mask], columns=columns)])
                mongo_filter["stock"] = {"$in": as_list(_index[missing_mask].astype(int))}
            else:
                logger.debug(f"all strengths found")
                return strengths.loc[_index.astype(str)]

        # if no indices are specified, check which of all strengths are missing
        else:
            logger.debug("checking for missing strengths")
            _all_ids = pd.Index(self.get_ids("1") + self.get_ids("2") + self.get_rejected_ids()).astype(str)
            logger.debug(f"found {len(_all_ids)} IDs")
            missing_ids = _all_ids[~_all_ids.isin(strengths.index.astype(str))]
            logger.debug(f"found {len(missing_ids)} missing strengths")
            if len(missing_ids) < 1e6:
                logger.debug(f"only querying for {len(missing_ids)} missing strengths")
                mongo_filter["stock"] = {"$in": as_list(missing_ids)}
            else:
                logger.debug("more than 1e6 missing, querying for all strengths")
            strengths = pd.concat([strengths, pd.DataFrame(index=missing_ids, columns=columns)])

        # get the strengths
        logger.debug("getting strengths")
        for i, x in tqdm(enumerate(self.t2collection.find(mongo_filter)), desc="getting strengths"):
            stock = str(x["stock"])
            for band in ["W1", "W2"]:
                res = x["body"][-1][f"Wise_{band}"]
                strengths.loc[stock, f"{band}_strength"] = res["strength_sjoert"]
                strengths.loc[stock, f"{band}_pre_flare_var_sig"] = res["significance"]

        if ((not use_all_indices) and missing_mask.any()) or use_all_indices:
            strengths["min_strength"] = strengths[["W1_strength", "W2_strength"]].min(axis=1)
            strengths["max_var"] = strengths[["W1_pre_flare_var_sig", "W2_pre_flare_var_sig"]].max(axis=1)
            strengths["W1_strength_by_var"] = strengths["W1_strength"] / strengths["W1_pre_flare_var_sig"]
            strengths["W2_strength_by_var"] = strengths["W2_strength"] / strengths["W2_pre_flare_var_sig"]
            strengths["min_strength_by_var"] = strengths[["W1_strength_by_var", "W2_strength_by_var"]].min(axis=1)
            logger.debug(f"saving {len(strengths)} strengths to {filename}")
            strengths.to_json(filename)

        if not use_all_indices:
            strengths = strengths.loc[_index.astype(str)]

        return strengths

    def get_t2_dust_echo_eval_values(self, index: Index, value: str) -> pd.DataFrame:
        """
        Get a value per filter and lightcurve as produced by the :class:`AMPEL` :class:`T2DustEchoEval`

        :param index: The index of the lightcurves
        :type index: Index
        :param value: The key of the value
        :type value: str
        :return: The value per lightcurves and filter
        :rtype: pandas.DataFrame
        """

        indices = as_list(index)
        logger.debug(f"getting {value} for {len(indices)} objects of {self.base_name} in {self.database_name}")

        filter = {
            "unit": "T2DustEchoEval",
            "stock": {"$in": as_list(index)},
            "code": 0
        }

        n = self.t2collection.count_documents(filter)
        logger.debug(f"found {n} documents")

        values = dict()

        for lc in self.t2collection.find(filter):
            ivalue = dict()

            for i, b in enumerate(["W1", "W2"]):
                try:
                    ivalue[f"{value}_{b}"] = lc["body"][-1]["values"][value][i]
                except KeyError as e:
                    raise KeyError(f"{lc}: {e}")
                except IndexError as e:
                    raise IndexError(f"{lc}: {e}")

            values[str(lc["stock"])] = ivalue

        logger.debug(f"returning {len(values)} results")

        return pd.DataFrame.from_dict(values, orient="index")

    def get_peak_time_jd(self, index: Index) -> pd.DataFrame:
        """Get the peak time in Julian Days"""
        return self.get_t2_dust_echo_eval_values(index, "max_mag_jd")

    def get_excess_end_jd(self, index: Index) -> pd.DataFrame:
        """Get the start of the excess in Julian Days"""
        return self.get_t2_dust_echo_eval_values(index, "excess_jd")

    def get_dust_echo_strength(self, index: Index) -> pd.DataFrame:
        """
        Get the strength of the dust echo.
        .. note::
            This will only work if the object is status 1 or 2. If you want the strength for any object,
            use :meth:`get_strength` instead.
        """
        return self.get_t2_dust_echo_eval_values(index, "strength_sjoert")

    def get_fade_time(self, index: Index) -> pd.DataFrame:
        """Get the fade time"""
        return self.get_t2_dust_echo_eval_values(index, "e_fade")

    def get_rise_time(self, index: Index) -> pd.DataFrame:
        """Get the rise time"""
        return self.get_t2_dust_echo_eval_values(index, "e_rise")

    #
    # ------------------     get T2DustEchoEval results       -------------------- #
    # --------------------------------   END   ----------------------------------- #
    ################################################################################

    ############################################################################################
    # -------------     get T2CatalogMatch and T2DigestRedshifts results       --------------- #
    # -------------------------------------  START  ------------------------------------------ #
    #

    def get_catalog_matches(self, index: Index, code: int = 0) -> dict:
        """
        Get the matches as determined by the :class:`AMPEL` :class:`T2CatalogMatch`

        :param index: Index of the Lightcurves
        :type index: Index
        :param code: The document code to query for
        :type code: int
        :return: All matches in the catalogues
        :rtype: dict
        """
        logger.debug(f"getting catalog match info for {self. base_name} in {self.database_name}")
        indices = as_list(index)
        logger.debug(f"getting catalog match info for {len(indices)} objects")

        matches = dict()

        for chunked_indices in chunks(indices, 1000000):

            filter = {
                "code": code,
                "stock": {"$in": chunked_indices},
                "unit": "T2CatalogMatch"
            }

            for i in self.t2collection.find(filter):
                matches[i["stock"]] = i["body"][-1]

        return matches

    def get_redshift(self, index: Index, code: int = 0) -> pd.DataFrame:
        """
        Get the redshifts as determined by the :class:`AMPEL` :class:`T2DigestRedshifts`

        :param index: Index of the lightcurves
        :type index: Index
        :param code: The document code to query T2CatalogMatch results to get match names
        :type code: int
        :return: The redshift, distance to the match and the uncertainty associated to the redshift measurement method
        :rtype: pandas.DataFrame
        """
        filter = {
            "unit": "T2DigestRedshifts",
            "stock": {"$in": as_list(index)},
        }

        n = self.t2collection.count_documents(filter)
        logger.debug(f"found {n} documents")

        redshift_keys = {
            "NEDz_extcats": {"spec": "z"},
            "SDSS_spec": {"spec": "z"},
            "GLADEv23": {"spec": "z"},
            "LSPhotoZZou": {"photo": "photoz", "spec": "specz"},
            "wiseScosPhotoz": {"photo": "zPhoto_Corr"},
            "twoMPZ": {"photo": "zPhoto", "spec": "zSpec"},
            "PS1_photoz": {"photo": "z_phot"},
            "NEDz": {"spec": "z"},
        }

        redshift = dict()
        matches = self.get_catalog_matches(index, code)

        for lc in self.t2collection.find(filter):
            try:
                if "ampel_z" in lc["body"][-1]:

                    # find the redshift as calculated by AMPEL T2DigestRedshift
                    d = {k: lc["body"][-1][k] for k in ["ampel_z", "ampel_dist", "group_z_precision"]}
                    redshift[str(lc["stock"])] = d

                    # find the redshifts that were used to calculate the AMPEL redshift
                    group_zs = lc["body"][-1]["group_zs"]
                    if all([len(g) for g in group_zs]):
                        raise ValueError(f"no group_zs found for {lc['stock']}")
                    for group_z in group_zs:
                        if len(group_z) > 0:
                            break

                    # find the catalog matches that provided the redshifts
                    redshift_catalogs = []
                    for catalog, result in matches[int(lc["stock"])].items():
                        if (result is not None) and (catalog in redshift_keys):
                            redshifts = [result[k] for k in redshift_keys[catalog].values() if k in result]
                            if any([z in redshifts for z in group_z]):
                                redshift_catalogs.append(catalog)
                    if len(redshift_catalogs) == 0:
                        raise ValueError(f"no redshift catalog found for {lc['stock']}")
                    redshift[str(lc["stock"])]["catalogs"] = ", ".join(redshift_catalogs)

                else:
                    redshift[str(lc["stock"])] = {"ampel_z": np.nan, "ampel_dist": np.nan, "group_z_precision": np.nan}
            except KeyError as e:
                raise KeyError(f"{lc}: {e}")

        logger.debug(f"returning {len(redshift)} results")

        return pd.DataFrame.from_dict(redshift, orient="index")

    #
    # -------------     get T2CatalgueMatch and T2DigestRedshifts results       --------------- #
    # --------------------------------------   END   ------------------------------------------ #
    #############################################################################################

#
# -----------------------      DatabaseConnector       ----------------------- #
# --------------------------------   END   ----------------------------------- #
################################################################################
