#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
High level I/O utility methods for pyaerocom
"""

from pyaerocom.io.aerocom_browser import AerocomBrowser
from pyaerocom.io.readgridded import ReadGridded
from pyaerocom.io.readungridded import ReadUngridded
from pyaerocom import const, change_verbosity

def browse_database(model_or_obs, verbose=False):
    if not verbose:
        change_verbosity('critical')
    else:
        change_verbosity('debug')
    browser = AerocomBrowser()
    matches = browser.find_matches(model_or_obs)
    if len(matches) is 0:
        print('No match could be found for {}'.format(model_or_obs))
        return
    elif len(matches) > 20:
        print('Found more than 20 matches for based on input string {}:\n\n'
              'Matches: {}\n\n'
              'To receive more detailed information, please specify search ID '
              'more accurately'.format(model_or_obs, matches))
        return
    for match in matches:
        if match in const.OBS_IDS:
            reader = ReadUngridded(match)
        else:
            reader = ReadGridded(match)
        print(reader)
    

if __name__=='__main__':
    
    obs_id = 'AATSR*'
    
    browse_database('AATSR_SU*')
    
    browse_database('AATSR*ORAC*v4*')
    
    browse_database(obs_id)