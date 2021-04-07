"""
Test script for creating variables.ini from HTAP2 excel table
"""
import openpyxl
import string
from collections import OrderedDict as od
from configparser import ConfigParser
import os
tab = 'HTAP2_variables.xlsx'

config = 'variables.ini'

IGNORE = ['freq', 'priority']
if __name__=='__main__':

    book = openpyxl.load_workbook(tab)

    #read sheet Surface
    sheets = ['Surface', 'Column', 'ModelLevel',
              'SurfAtStations (Aerosol)', 'SurfAtStations (Gas)',
              'ModelLevelAtStations']

    cols = ['var_name', 'description', 'standard_name', 'var_type',
                'unit', 'minimum', 'maximum', 'dimensions', 'freq',
                'priority', 'comments_and_purpose']

    result = od()
    multiple = {}
    for sheet_name in sheets:
        sheet = book[sheet_name]
        col_names = string.ascii_uppercase[:len(cols)]

        CTRL_COL = 'C'

        for i, item in enumerate(sheet['A']):

            if sheet[CTRL_COL][i].value is None:
                continue

            var_spec = od()
            var_name = item.value
            if var_name.startswith('HTAP'):
                continue
            if var_name in result:
                try:
                    multiple[var_name] += 1
                except KeyError:
                    multiple[var_name] = 1
                continue
            for j, col in enumerate(col_names):
                val = sheet[col][i].value
                var_spec[cols[j]] = val

            result[var_name] = var_spec

    #df = pd.DataFrame(list(result.values()), columns=cols)
    #df.to_csv(config)

    if not os.path.exists(config):
        open(config, 'a')

    cfg = ConfigParser()
    cfg.read(config)

    errs = {}
    for var, info in result.items():
        if not var in cfg:
            cfg.add_section(var)
        for k, v in info.items():
            if k in IGNORE:
                continue
            try:
                cfg.set(var, k, str(v))
            except ValueError as e:
                errs[var] = '{}: {}'.format(k, repr(e))
    with open(config, 'w') as f:
        cfg.write(f)

    for var, err in errs.items():
        print('{}: {}'.format(var, err))
