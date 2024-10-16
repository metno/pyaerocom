# Example aeroval configuration for pm ratios
# using the EMEP reader (which has a built in pm ratio calculation)

import os
from getpass import getuser

from pyaerocom.aeroval import EvalSetup, ExperimentProcessor
from pyaerocom.aeroval.config.pmratios.base_config import get_CFG

reportyear = year = 2019
CFG = get_CFG(reportyear=reportyear, year=year,
              # model directory
              model_dir="/lustre/storeB/project/fou/kl/CAMEO/u8_cams0201/"
              )
user = getuser()

CFG.update(dict(
    json_basedir=os.path.abspath(f"/home/{user}/data/aeroval-local-web/data"),  # always adjust to your environment
    coldata_basedir=os.path.abspath(f"/home/{user}/data/aeroval-local-web/coldata"),
    # always adjust to your environment
    clear_existing_json=True,
    add_model_maps=True,
    # if True, the analysis will stop whenever an error occurs (else, errors that
    # occurred will be written into the logfiles)
    raise_exceptions=False,
    modelmaps_opts=dict(maps_freq="monthly", maps_res_deg=5),
    # Regional filter for analysis
    periods=[f"{year}"],
    proj_id="RATPM",
    exp_id=f"ratpm testing {year}",
    exp_name=f"Evaluation of EMEP runs for {year}",
    exp_descr=(
        f"Evaluation of EMEP runs for {year} for CAMEO. The EMEP model, is compared against observations from EEA and EBAS."
    ),
    exp_pi="jang@met.no",
    public=True,
    # directory where colocated data files are supposed to be stored
    weighted_stats=True, ))

stp = EvalSetup(**CFG)

ana = ExperimentProcessor(stp)
ana.update_interface()

res = ana.run()
