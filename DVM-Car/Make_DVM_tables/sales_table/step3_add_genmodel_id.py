import sys
import numpy as np
from own_pathes import own_path_d
sys.path.append(own_path_d['DVM_tools'])
from CarModelMatcher import CarModelMatcher

raw_file_pa = 'Projects/DVM/New_DVM/DVM_tables/prepare_DVM_tables/sales_table/ws_dstore/output/genmodel_sales_19_12_25_2.csv'
genmodel_tab_pa = 'Lib/py3_lib/DVM_tools/genmodel_table.csv'
new_matcher = CarModelMatcher(genmodel_tab_pa, print_error=False)
output_file_pa = 'Projects/DVM/New_DVM/DVM_tables/prepare_DVM_tables/sales_table/ws_dstore/output/shared_sales_v2_191225.csv'


with open(output_file_pa, 'w') as f_out:
    with open(raw_file_pa, 'r') as f_in:
        cont = f_in.readlines()
        header = cont[0].strip().split(',')
        header.insert(2, 'Matched_genmodel_ID')
        f_out.write(','.join(header) + '\n')

        for line in cont[1:]:
            pieces = line.strip().split(',')
            maker_str, genmodel_str = pieces[:2]
            if 'Missing' in genmodel_str or 'Unknown' in genmodel_str:
                continue

            ten_year_sold = [int(float(ele)) for ele in pieces[3:15] if len(ele) > 0 ]

            try:
                matched_maker, matched_genmodel, matched_id = new_matcher.find_maker_and_model(
                    maker_str, genmodel_str, with_genmodel_id=True)

                pieces.insert(2, matched_id)
                f_out.write(','.join(pieces) + '\n')
            except:
                ten_year_sold_num = sum(ten_year_sold)
                if ten_year_sold_num > 500:
                    print('error ', maker_str,'|||', genmodel_str, ten_year_sold_num)
                pieces.insert(2, '')

