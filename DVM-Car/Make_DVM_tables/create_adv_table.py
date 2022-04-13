from DataFileDealer import DataFileDealer
from LoadOrWriteObj import write_or_read_obj
from copy import copy


def get_year_month(in_str):
    year = in_str[:4]
    month = in_str[4:6]
    return year, month


def write_new_csv(header_l, pieces, year, month, new_adv_id):
    pieces[header_l.index('Adv_ID')] = new_adv_id
    pieces.insert(4, month)
    pieces.insert(4, year)
    with open('new_file.csv', 'a') as f_out:
        out_line = ','.join(pieces) + '\n'
        f_out.write(out_line)


raw_adv_file_pa = 'New_DVM/DVM_tables/prepare_DVM_tables/advert_table/ws_dstore/whole_adv_table.csv'
unwanted_attr_l = ['Seller_type', 'Location', 'Height', 'Width', 'Length']
data_file_dealer = DataFileDealer()
header_l, cont_l = data_file_dealer.read_file(raw_adv_file_pa, unwanted_attr_l)
adv_id_d = {}

write_new_csv(header_l, copy(header_l), 'Adv_year', 'Adv_month', 'Adv_ID')

for pieces in cont_l:
    t_adv_id = pieces[header_l.index('Adv_ID')]
    gen_id = pieces[header_l.index(' Genmodel_id')]

    year, month = get_year_month(t_adv_id)

    if gen_id not in adv_id_d:
        adv_id_d[gen_id] = []

    adv_id_d[gen_id].append(t_adv_id)
    new_adv_id = gen_id + '$$' +str(len(adv_id_d[gen_id]))
    # pieces[header_l.index('Adv_ID')] = new_adv_id
    write_new_csv(header_l, pieces, year, month, new_adv_id)

write_or_read_obj('adv_dict', adv_id_d)