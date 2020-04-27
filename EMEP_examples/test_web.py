# -*- coding: utf-8 -*-

import pyaerocom as pya
from pyaerocom.web.aerocom_evaluation import AerocomEvaluation
from pyaerocom.web.trends_evaluation import TrendsEvaluation
from pyaerocom.io.readgridded import ReadGridded

aaspath = '/home/eirikg/Desktop/pyaerocom/data/aas'
pya.const.add_ungridded_obs('aas', aaspath, reader=pya.io.ReadAasEtal)

emep_path = '/home/eirikg/Desktop/pyaerocom/data/2020_AerocomHIST'
pya.const.add_data_search_dir(emep_path)

cfg_dir = 'conf'


# Evaluation

stp = AerocomEvaluation(proj_id='test', exp_name='testing', exp_id='test_exp', config_dir=cfg_dir)


obs_config = {'aas': dict(obs_id='aas',
                                obs_vars='wetso4',
                                vert_scheme='Surface',
                                obs_vert_type='Surface')}

model_config = {'emep': dict(model_id='processed',
                             model_ts_type_read='monthly',
                             mtype='?')}


stp.obs_config = obs_config                  
stp.model_config = model_config

colset=stp.colocation_settings
colset['filter_name'] = 'WORLD-wMOUNTAINS'
colset['obs_id'] = 'aas'
colset['model_id'] = 'processed'
colset['start'] = 2010
# colset['stop'] = 
colset['colocate_time'] = True
colset['model_ts_type_read'] = 'monthly'
colset['ts_type'] = 'monthly'

stp.run_evaluation()

stp.make_info_table_web()
    
stp.make_regions_json()


# Trends
t = TrendsEvaluation(out_basedir='/home/eirikg/JSON',periods=['2010-2010'],name='test_trends', model_config=model_config, obs_config=obs_config)
t.run_evaluation()