#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script that converts IDL EBAS import settings to ini file that is used in
pyaerocom for EBAS I/O
"""
from collections import OrderedDict as od
FILE_IDL = 'aerocom_read_include.txt'

list_info_lines = {'c_Component'            : 'component',
                   'c_Instrument'           : 'instrument',
                   'c_Matrix'               : 'matrix'  ,
                   'c_AdditionalVarNames'   : 'requires',
                   'f_ScaleFactor'          : 'scale_factor'}
if __name__=="__main__":

    result = od()
    
    read_idx = []
    for line in open(FILE_IDL):
        if line.startswith('tC_EBASVars['):
            try:
                
                num = int(line.split('[')[1].split(']')[0])
            except:
                print('Failed line {}'.format(line))
                
            if not num in result:
                print('New variable (no. {})'.format(num))
                result[num] = od()
            if 'c_ModelVar' in line:
                var = line.split('=')[1].strip()
                result[num]['var_name'] = var[1:-1]
            else:
                
                for sub in list_info_lines:
                    if sub in line:
                        name = list_info_lines[sub]
                        spl = line.split('=')[1].split('[')[1].split(']')[0]
                        res = []
                        for val in spl.split(','):
                            val = val.strip()
                            if "'" in val or '"' in val:
                                #val is string
                                val = val[1:-1]
                        
                            res.append(val)
                        print(res)
                        result[num][name] = res
                        
    cfg = open('ebas_config.ini', 'w')        
    for num, info in result.items():
        cfg.write('[' + info['var_name']  +']\n')
        for name in list_info_lines.values():
            if name in info:
                print(name)
                print(info[name])
                val = ','.join(item for item in info[name])
                cfg.write('{}={}\n'.format(name, val))
        cfg.write('\n')
    cfg.close()
        