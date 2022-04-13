import sys
import numpy as np
from own_pathes import own_path_d
sys.path.append(own_path_d['DVM_tools'])
from CarModelMatcher import CarModelMatcher


raw_file_pa = 'Projects/DVM/New_DVM/DVM_tables/prepare_DVM_tables/sales_table/ws_dstore/raw/veh0126_2019.csv'
# genmodel_tab_pa = 'Lib/py3_lib/DVM_tools/genmodel_table.csv'
# new_matcher = CarModelMatcher(genmodel_tab_pa)
def sum_up_sales(sum_array, in_l):
    new_l = []
    for ele in in_l:
        if len(ele) == 0:
            new_l.append(0)
        else:
            new_l.append(int(ele))

    sum_array = sum_array + np.array(new_l)
    return sum_array


def merge_genmodel():
    year_len = 19
    t_genmodel_summary = [None, np.zeros(year_len), None]
    output_fpa = 'Projects/DVM/New_DVM/DVM_tables/prepare_DVM_tables/sales_table/ws_dstore/output/genmodel_sales_19_12_25_1.csv'
    f_out = open(output_fpa, 'w')

    with open(raw_file_pa, 'r') as f_in:
        cont = f_in.readlines()
        header_l = cont[0].strip().split(',')
        f_out.write(','.join(header_l[:2] + header_l[3:3+year_len]) + '\n')

        for line in cont[1:]:

            pieces = line.strip().split(',')
            t_genmodel = pieces[1]

            if t_genmodel_summary[0] is None:
                t_genmodel_summary[0] = t_genmodel
                t_genmodel_summary[2] = pieces[0]

            if t_genmodel != t_genmodel_summary[0]:

                f_out.write(','.join([t_genmodel_summary[2], t_genmodel_summary[0]]+[str(ele) for ele in list(t_genmodel_summary[1])])+'\n')
                t_genmodel_summary = [t_genmodel, np.zeros(year_len), pieces[0]]

            t_genmodel_summary[1] = sum_up_sales(t_genmodel_summary[1], pieces[3:3+year_len])


merge_genmodel()