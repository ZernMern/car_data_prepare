class DataFileDealer:
    def __init__(self):
        self.unwanted_idx_l = None

    def remove_unwated(self, in_l):
        for ele in self.unwanted_idx_l:
            in_l.pop(ele)
        return in_l

    def get_idx_of_unwanted(self, header_l, unwanted_l):
        idx_s = set()
        for word in unwanted_l:
            if word not in header_l:
                print('Error, not found word', word)
                continue
            idx_s.add(header_l.index(word))
        return sorted(list(idx_s))[::-1]

    def read_file(self, in_f_pa, unwanted_l=None):
        rst_l = []
        with open(in_f_pa, 'r') as f_in:
            cont = f_in.readlines()
            header_l = cont[0].strip().split(',')

            if unwanted_l is not None:
                self.unwanted_idx_l = self.get_idx_of_unwanted(header_l, unwanted_l)
                header_l = self.remove_unwated(header_l)

            for line in cont[1:]:
                pieces = line.strip().split(',')
                if unwanted_l is not None:
                    pieces = self.remove_unwated(pieces)
                rst_l.append(pieces)

            return header_l, rst_l