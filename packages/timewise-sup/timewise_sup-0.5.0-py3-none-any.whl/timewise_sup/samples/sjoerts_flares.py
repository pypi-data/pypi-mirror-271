import logging
import pandas as pd
from pathlib import Path
from timewise import ParentSampleBase, WISEDataDESYCluster

from timewise_sup.config_loader import TimewiseSUPConfig
from timewise_sup.mongo import DatabaseConnector, Index


logger = logging.getLogger(__name__)

sjoerts_base_name = "sjoerts_flares"
sjoerts_database_name = sjoerts_base_name


def get_test_flares_config():
    config = TimewiseSUPConfig(
        database_name=sjoerts_database_name,
        wise_data=TestWISEData()
    )
    return config


class TestWISEData(WISEDataDESYCluster):

    def __init__(self, **kwargs):
        super(TestWISEData, self).__init__(
            base_name=TestParentSample.base_name,
            parent_sample_class=TestParentSample,
            n_chunks=2,
            min_sep_arcsec=6
        )

    def submit_to_cluster(
            self,
            node_memory,
            single_chunk=None,
            mask_by_position=False
    ):
        logger.info("emulating cluster work")

        # from timewise/wise_bigdata_desy_cluster.py
        if isinstance(single_chunk, type(None)):
            _start_id = 1
            _end_id = int(self.n_chunks*self.n_cluster_jobs_per_chunk)
        else:
            _start_id = int(single_chunk*self.n_cluster_jobs_per_chunk) + 1
            _end_id = int(_start_id + self.n_cluster_jobs_per_chunk) - 1

        logger.debug(f"Jobs from {_start_id} to {_end_id}")

        for job_id in range(_start_id, _end_id+1):
            logger.debug(f"Job {job_id}")
            chunk_number = self._get_chunk_number_for_job(job_id)
            self._subprocess_select_and_bin(service='tap', chunk_number=chunk_number, jobID=job_id)
            self.calculate_metadata(service='tap', chunk_number=chunk_number, jobID=job_id)

        return 1

    def wait_for_job(self, job_id=None):
        logger.info("called dummy wait for cluster")


class TestParentSample(ParentSampleBase):

    base_name = sjoerts_base_name

    default_keymap = {
        "ra": "ra",
        "dec": "dec",
        "id": "name",
        "W1_mag": "w1mpro",
        "W2_mag": "w2mpro",
    }

    def __init__(self):
        logger.info("initialising test ParentSample")
        super(TestParentSample, self).__init__(base_name=TestParentSample.base_name)
        self.df = self.sample()

    def get_redshifts(self, index: Index) -> pd.DataFrame:
        redshifts = self.df.loc[index, ["z"]]
        redshifts = redshifts[redshifts != '–'].astype(float)
        redshifts = redshifts[~redshifts["z"].isna()]
        redshifts["z_unc"] = redshifts["z"] * 0.01
        redshifts.set_index(redshifts.index.astype(str), inplace=True)
        return redshifts

    @staticmethod
    def sample():
        data_file = Path(__file__).parent / "data" / "test_sample.json"
        logger.debug(f"reading sample from {data_file}")
        _df = pd.read_json(data_file, orient="index")
        _df.index = _df.index.astype(int)
        return _df
