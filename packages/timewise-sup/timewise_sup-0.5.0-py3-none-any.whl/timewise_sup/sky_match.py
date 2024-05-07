import logging
import os
import pandas as pd
from timewise.wise_data_base import WISEDataBase

from timewise_sup.mongo import DatabaseConnector
from timewise_sup.environment import load_environment

try:
    import k3match
except ImportError:
    k3match = None


logger = logging.getLogger(__name__)


def manual_match(
        wise_data: WISEDataBase,
        catalogue_name: str,
        ra_field_name: str | list[str | int],
        dec_field_name: str | list[str | int],
        name_field_name: str | list[str | int],
        radius_arcsec: float,
        catalogue_database_name: str = None,
        catalogue_collection_name: str = None,
        catalogue_filename: str = None,
        catalogue_dataframe: pd.DataFrame = None
):

    base_name = wise_data.base_name
    tsup_data_dir = load_environment("TIMEWISE_SUP_DATA")
    fn = os.path.join(tsup_data_dir, "sky_match", f"{base_name}_{catalogue_name}_{radius_arcsec:.1f}arcsec.csv")

    if not os.path.isfile(fn):
        logger.debug(f"{fn} not found")

        if k3match is None:
            raise ImportError(
                f"k3match not found! Please make sure to install it: "
                f"https://pschella.github.io/k3match/index.html"
            )

        field_names_list = [
            ra_field_name,
            dec_field_name,
            name_field_name
        ]

        out_colum_list = ["ra", "dec", "name"]

        logger.info(f"loading {catalogue_name}")

        if catalogue_dataframe is not None:
            rename = {k1: k2 for k1, k2 in zip(field_names_list, out_colum_list)}
            catalogue = catalogue_dataframe.rename(columns=rename)

        elif catalogue_database_name is not None:
            logger.debug(f"loading {catalogue_database_name} from database")
            rename = {f"field{i}": k for i, k in enumerate(out_colum_list)}
            database_connector = DatabaseConnector(base_name=base_name, database_name=catalogue_database_name)
            catalogue = database_connector.get_dataframe(
                field_name_lists=field_names_list,
                collection_name=catalogue_collection_name,
            ).rename(columns=rename)

        elif catalogue_filename is not None:
            logger.debug(f"loading {catalogue_filename}")
            rename = {k1: k2 for k1, k2 in zip(field_names_list, out_colum_list)}
            catalogue = pd.read_csv(
                catalogue_filename,
                usecols=field_names_list
            ).rename(columns=rename)

        else:
            raise ValueError(
                "Either of catalogue_dataframe, catalogue_database_name or catalogue_filename must be given!"
            )

        logger.info(f"done")

        sample = wise_data.parent_sample.df

        logger.info(f"spatially matching {wise_data.base_name} against {catalogue_name}, (radius={radius_arcsec:.2f} arcsec)")
        id_sample, id_catalogue, dist = k3match.celestial(
            sample[wise_data.parent_sample.default_keymap["ra"]],
            sample[wise_data.parent_sample.default_keymap["dec"]],
            catalogue["ra"],
            catalogue["dec"],
            radius_arcsec * 1 / 3600  # convert to degrees
        )
        logger.info(f"found {len(id_sample)} matches")

        skymatch_df = pd.DataFrame({
            f"{base_name}": id_sample,
            f"{catalogue_name}": id_catalogue,
            f"{catalogue_name}_name": catalogue["name"][id_catalogue],
            "dist": dist
        })
        logger.debug(f"saving to {fn}")

        _dir = os.path.dirname(fn)
        if not os.path.isdir(_dir):
            os.makedirs(_dir)

        skymatch_df.to_csv(fn)

    else:
        logger.info(f"loading {fn}")
        skymatch_df = pd.read_csv(fn, index_col=0)

    return skymatch_df
