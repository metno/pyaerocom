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
    in_multi_line_list = False
    list_temp = None
    num_temp = None
    name_temp = None
    for line in open(FILE_IDL):
        line = line.strip().split(';')[0]
        if not line:
            continue
        if in_multi_line_list:
            delim ='$'
            if not line.endswith('$'):
                in_multi_line_list = False
                delim = ']'
                if not line.endswith(']'):
                    raise IOError(line)
            spl = line.split(delim)[0]
            for val in spl.split(','):
                val = val.strip()
                if "'" in val or '"' in val:
                    #val is string
                    val = val[1:-1]
                if val:
                    list_temp.append(val)
                    print(list_temp)
            if delim == ']':
                result[num_temp][name_temp] = list_temp
        elif line.startswith('tC_EBASVars['):
            try:
                num = int(line.split('[')[1].split(']')[0])
            except:
                print('Failed line {}'.format(line))
                
            if not num in result:
                print('New variable (no. {})'.format(num))
                result[num] = od()
            if 'c_ModelVar' in line:
                var = line.split('=')[1].strip()[1:-1]
                result[num]['old_name'] = var
                name = var.lower()
                if '_' in name:
                    name = "".join(name.split('_'))
                result[num]['var_name'] = name
            else:
                for sub in list_info_lines:
                    if sub in line:
                        name = list_info_lines[sub]
                        spl = line.split('=')[1].split('[')[1]
                        if line.endswith('$'):
                            print("Reached multiline list def: {}".format(name))
                            in_multi_line_list = True
                            name_temp = name
                            num_temp = num
                            spl = spl.split('$')[0]
                            list_temp = []
                            for val in spl.split(','):
                                val = val.strip()
                                if "'" in val or '"' in val:
                                    #val is string
                                    val = val[1:-1]
                                if val:
                                    list_temp.append(val)
                            print(list_temp)
                        else:
                            spl = spl.split(']')[0]
                            res = []
                            for val in spl.split(','):
                                val = val.strip()
                                if "'" in val or '"' in val:
                                    #val is string
                                    val = val[1:-1]
                            
                                res.append(val)
                            #print(res)
                            result[num][name] = res
                            
    cfg = open('ebas_config.ini', 'w')        
    for num, info in result.items():
        cfg.write('[' + info['var_name']  +']\n')
        cfg.write('old_name={}\n'.format(info['old_name']))
        for name in list_info_lines.values():
            if name in info:
                items = list(dict.fromkeys(info[name]))
                val = ','.join(item for item in items)
                cfg.write('{}={}\n'.format(name, val))
        cfg.write('\n')
    cfg.close()
        