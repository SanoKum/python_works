import sys
import numpy as np

def recursive_test(nnmap, i0, j_img, k_img, list_target, array_targeted, array_jk_set):
    print(i0)
    array_targeted[i0] = 1

    for i1 in nnmap[i0]:
        if (array_jk_set[i1] == 0):
            print("abs(i1-i0)",abs(i1-i0))
            if   (abs(i1-i0) == 4):
                j_img[i1] = j_img[i0]  
                k_img[i1] = k_img[i0] + np.sign(i1-i0)
            elif (abs(i1-i0) == 1): 
                j_img[i1] = j_img[i0] + np.sign(i1-i0) 
                k_img[i1] = k_img[i0] 
            else:
                print("Error: something wrong")
                sys.exit(1)

            array_jk_set[i1] = 1
        if (array_targeted[i1] == 0) and (i1 not in list_target):
            list_target.append(i1)

    print("  array_targeted",array_targeted)
    print("  array_jk_set  ",array_jk_set)
    print("  j_img         ",j_img)
    print("  k_img         ",k_img)


    if (len(list_target) != 0):
        inew = list_target[0]
        list_target.pop(0)
        recursive_test(nnmap, inew, j_img, k_img, list_target, array_targeted, array_jk_set)
    else:
        return 0
    


if __name__=="__main__":
    nnmap = [[1, 4], [0, 2, 5], [1, 3, 6], [2, 7], [0, 5, 8], [1,4,6,9], [2,5,7,10], \
            [3, 6, 11], [4,9], [5,8,10], [6,9,11], [7,10]]

    array_targeted = np.zeros(12, int)
    array_jk_set   = np.zeros(12, int)

    j_img          = np.zeros(12, int)
    k_img          = np.zeros(12, int)

    istart = 0
    list_target    = nnmap[istart]
    j_img[istart]  = 1
    k_img[istart]  = 1

    recursive_test(nnmap, istart, j_img, k_img, list_target, array_targeted, array_jk_set)

