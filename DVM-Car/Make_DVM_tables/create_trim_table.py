

def process_selling_time(in_str):
    if '/' in in_str:
        return in_str.split('/')[0]
    if '-' in in_str:
        return '20'+in_str.split('-')[1]
    print('not process year!')

def process_trim_name(in_str):
    if '(' in in_str:
        start_idx = in_str.index('(')
        end_idx = in_str.index(')')

        return in_str[:start_idx] + in_str[end_idx+1:]
    return in_str


def wirte_new_line(f_out, pieces):
    pieces.pop(6)
    pieces.pop(3)
    out_line = ','.join(pieces) + '\n'
    f_out.write(out_line)

file_pa = 'New_DVM/DVM_tables/prepare_DVM_tables/price_table/ws_dstore/price_table_view.csv'
t_s = set()
filter_attr = ['Generation1']
with open('new_one.csv', 'w') as f_out:
    with open(file_pa, 'r', encoding="ISO-8859-1") as f_in:
        cont = f_in.readlines()
        header_l = cont[0].strip().split(',')
        wirte_new_line(f_out, header_l)

        for line in cont[1:]:
            pieces = line.strip().split(',')
            pieces[5] = process_selling_time(pieces[5])  # Selling Year
            pieces[4] = process_trim_name(pieces[4]) + pieces[6]

            wirte_new_line(f_out, pieces)

print(t_s)