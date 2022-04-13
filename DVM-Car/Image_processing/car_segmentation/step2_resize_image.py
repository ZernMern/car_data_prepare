def get_useful_pic_set():
    pic_s = set()
    table_pa = 'New_DVM/DVM_tables/Image_table_updating/ws_dstore/image_table_useful_only_7_4-1.csv'
    with open(table_pa, 'r') as f_in:
        cont = f_in.readlines()

        for line in cont[1:]:
            pic_s.add(line.strip().split(',')[1])

    return pic_s


useful_pic_s = get_useful_pic_set()