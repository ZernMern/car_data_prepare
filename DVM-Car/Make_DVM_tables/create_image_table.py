from DataFileDealer import DataFileDealer
from LoadOrWriteObj import write_or_read_obj


def replace_pic_id(pieces):
    global ADV_D, MATCH_D
    old_adv_id = pieces[0].split('$$')[4]
    if old_adv_id not in MATCH_D:
        return None
    gen_id = MATCH_D[old_adv_id]

    new_adv_id = gen_id + '$$' + str(ADV_D[gen_id].index(old_adv_id) + 1)
    pieces[0] = pieces[0].replace(old_adv_id, new_adv_id)
    pieces.insert(0, gen_id)
    return pieces

def read_genmodel_id(old_adv_pa):
    match_d = {}
    with open(old_adv_pa, 'r') as f_in:
        cont = f_in.readlines()[1:]
        for line in cont:
            pieces = line.split(',')
            match_d[pieces[3]] = pieces[2]
    return match_d


def write_new_csv(pieces):
    with open('New_DVM/DVM_tables/Prepare_shared_dataset/shared_image_table.csv', 'a') as f_out:
        out_line = ','.join(pieces) + '\n'
        f_out.write(out_line)


image_table_pa = 'New_DVM/DVM_tables/Image_table_updating/ws_dstore/image_table_useful_only_7_4-1.csv'
old_adv_pa = 'New_DVM/DVM_tables/prepare_DVM_tables/advert_table/ws_dstore/whole_adv_table.csv'

data_dealer = DataFileDealer()
header_l, cont = data_dealer.read_file(image_table_pa, unwanted_l=['Pic_ID','Prob_car', 'Prob_wheel', 'Prob_bad_angle'])
hash_file_pa = 'New_DVM/DVM_tables/Prepare_shared_dataset/adv_hash_dict.pkl'

header_l.insert(0, 'Genmodel_ID')

write_new_csv(header_l)
ADV_D = write_or_read_obj(hash_file_pa)
MATCH_D = read_genmodel_id(old_adv_pa)
unfound_pic_num = 0


for pieces in cont:
    new_pieces = replace_pic_id(pieces)
    if new_pieces is None:
        unfound_pic_num += 1
        continue
    write_new_csv(new_pieces)

print(unfound_pic_num)