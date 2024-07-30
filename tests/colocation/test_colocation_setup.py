from pathlib import Path

import pytest
from pydantic import ValidationError

from pyaerocom import const
from pyaerocom.colocation.colocation_setup import ColocationSetup
from pyaerocom.config import ALL_REGION_NAME

COL_OUT_DEFAULT = Path(const.OUTPUTDIR) / "colocated_data"

default_setup = {
    "model_id": None,
    "obs_id": None,
    "obs_vars": (),
    # "obs_config": None,
    "ts_type": "monthly",
    "start": None,
    "stop": None,
    "filter_name": f"{ALL_REGION_NAME}-wMOUNTAINS",
    "basedir_coldata": COL_OUT_DEFAULT,
    "save_coldata": False,
    "obs_name": None,
    "obs_data_dir": None,
    "obs_use_climatology": False,
    "obs_cache_only": False,
    "obs_vert_type": None,
    "obs_ts_type_read": None,
    "obs_filters": {},
    "model_name": None,
    "model_data_dir": None,
    "model_read_opts": {},
    "read_opts_ungridded": {},
    "model_use_vars": {},
    "model_rename_vars": {},
    "model_add_vars": {},
    "model_to_stp": False,
    "model_ts_type_read": None,
    "model_read_aux": {},
    "model_use_climatology": False,
    "gridded_reader_id": {"model": "ReadGridded", "obs": "ReadGridded"},
    "flex_ts_type": True,
    "min_num_obs": None,
    "resample_how": "mean",
    "obs_remove_outliers": False,
    "model_remove_outliers": False,
    "zeros_to_nan": False,
    "obs_outlier_ranges": {},
    "model_outlier_ranges": {},
    "harmonise_units": False,
    "regrid_res_deg": None,
    "colocate_time": False,
    "reanalyse_existing": True,
    "raise_exceptions": False,
    "keep_data": True,
    "add_meta": {},
}


@pytest.mark.parametrize("stp,should_be", [(ColocationSetup(), default_setup)])
def test_ColocationSetup(stp: ColocationSetup, should_be: dict):
    stp_dict = stp.model_dump()
    for key, val in should_be.items():
        assert key in stp_dict
        if key == "basedir_coldata":
            assert Path(val) == Path(stp_dict["basedir_coldata"])
        else:
            assert val == stp_dict[key], key


def test_ColocationSetup_model_kwargs_validationerror() -> None:
    with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
        ColocationSetup(**default_setup, model_kwargs="not a dict")

    with pytest.raises(ValidationError, match="Key ts_type not allowed in model_kwargs "):
        ColocationSetup(**default_setup, model_kwargs={"emep_vars": {}, "ts_type": "daily"})
