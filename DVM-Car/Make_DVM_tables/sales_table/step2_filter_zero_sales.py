old_file_pa = 'Projects/DVM/New_DVM/DVM_tables/prepare_DVM_tables/sales_table/ws_dstore/output/genmodel_sales_19_12_25_1.csv'
new_file_pa = 'Projects/DVM/New_DVM/DVM_tables/prepare_DVM_tables/sales_table/ws_dstore/output/genmodel_sales_19_12_25_2.csv'
f_out = open(new_file_pa, 'w')

with open(old_file_pa, 'r') as f_in:
    cont = f_in.readlines()
    for line in cont:
        pieces = line.strip().split(',')
        sum_sales = sum([int(float(ele)) for ele in pieces[2:]])
        if sum_sales > 0 :
            f_out.write(line)