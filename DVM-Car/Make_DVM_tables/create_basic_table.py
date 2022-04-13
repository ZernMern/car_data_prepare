
def write_line(f_out, in_l):
    out_line = ','.join(in_l) + '\n'
    f_out.write(out_line)


orig_table_pa = 'Lib/py3_lib/DVM_tools/genmodel_table.csv'
removed_attr_l = ['Automaker_other_names', 'Genmodel_other_names', 'Trims', 'Body_type']
out_file_pa = 'Data/DVM_data/dataset_in_table_format/shared_basic_table.csv'

with open(out_file_pa, 'w') as f_out:
    with open(orig_table_pa, 'r') as f_in:
        cont = f_in.readlines()
        header_l = cont[0].strip().split(',')
        remove_idx_l = [header_l.index(attr) for attr in removed_attr_l]
        write_line(f_out, [header_l[i] for i in range(len(header_l)) if i not in remove_idx_l])

        for line in cont[1:]:
            line_pieces = line.strip().split(',')

            out_pieces = [ line_pieces[i] for i in range(len(line_pieces)) if i not in remove_idx_l]
            write_line(f_out, out_pieces)