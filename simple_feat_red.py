import numpy as np
import os
import sys

features = ["class"] +\
           ["ratetot_num", "ratetot_sz"] +\
           ["ratet_num_" + str(i) for i in range(3)] +\
           ["ratet_sz_" + str(i) for i in range(3)] +\
           ["rate_num_" + str(i) for i in range(64)] +\
           ["rate_sz_" + str(i) for i in range(64)] +\
           ["fract_num_" + str(i) for i in range(3)] +\
           ["fract_sz_" + str(i) for i in range(3)] +\
           ["frac_num_" + str(i) for i in range(64)] +\
           ["frac_sz_" + str(i) for i in range(64)] +\
           ["sratt_num_" + str(i) for i in range(3)] +\
           ["sratt_sz_" + str(i) for i in range(3)] +\
           ["srat_num_" + str(i) for i in range(64)] +\
           ["srat_sz_" + str(i) for i in range(64)] +\
           ["ltot_sz"] +\
           ["lt_sz_" + str(i) for i in range(3)] +\
           ["l_sz_" + str(i) for i in range(64)] +\
           ["sdtot"] +\
           ["sdt_sz_" + str(i) for i in range(3)] +\
           ["sd_sz_" + str(i) for i in range(64)]

if __name__ == '__main__':
    feature_path = sys.argv[1]
    reduced_path = sys.argv[2]
    header_path = sys.argv[3]
    data_array = []
    comb_array = []
    files = os.listdir(feature_path)
    for fn in files:
        curr_array = []
        with open(os.path.join(feature_path, fn)) as f:
            curr_array.extend(map(lambda l: l.strip().split(), f.readlines()))
        data_array.append(curr_array)
        comb_array += curr_array

    sd_array = np.array(comb_array, dtype=float).std(axis=0)
    zeros = [cn for cn, sdev in enumerate(sd_array) if sdev < 0.00001]
    remaining = [feat for i, feat in enumerate(features) if i not in zeros][1:]

    print("Remaining Features: ")
    print(remaining)

    with open(header_path, 'w+') as f:
        for feat in remaining:
            f.write(feat + '\n')

    for i, fn in enumerate(files):
        with open(os.path.join(reduced_path, fn), 'w+') as f:
            arr = data_array[i]
            arr = np.delete(arr, zeros, axis=1)
            f.write('\n'.join(map(lambda r: ' '.join(r), arr)))
            f.write('\n')
