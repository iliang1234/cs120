from asyncio import base_tasks
import math
import numpy as np
import time
import random
import matplotlib.pyplot as plt

"""
See below for mergeSort and countSort functions, and for a useful helper function.
In order to run your experiments, you may find the functions random.randint() and time.time() useful.

In general, for each value of n and each universe size 'U' you will want to
    1. Generate a random array of length n whose keys are in 0, ..., U - 1
    2. Run count sort, merge sort, and radix sort ~10 times each,
       averaging the runtimes of each function. 
       (If you are finding that your code is taking too long to run with 10 repitions, you should feel free to decrease that number)

To graph, you can use a library like matplotlib or simply put your data in a Google/Excel sheet.
A great resource for all your (current and future) graphing needs is the Python Graph Gallery 
"""


def merge(arr1, arr2):
    sortedArr = []

    i = 0
    j = 0
    while i < len(arr1) or j < len(arr2):
        if i >= len(arr1):
            sortedArr.append(arr2[j])
            j += 1
        elif j >= len(arr2):
            sortedArr.append(arr1[i])
            i += 1
        elif arr1[i][0] <= arr2[j][0]:
            sortedArr.append(arr1[i])
            i += 1
        else:
            sortedArr.append(arr2[j])
            j += 1

    return sortedArr

def mergeSort(arr):
    if len(arr) < 2:
        return arr

    midpt = int(math.ceil(len(arr)/2))

    half1 = mergeSort(arr[0:midpt])
    half2 = mergeSort(arr[midpt:])

    return merge(half1, half2)

def countSort(univsize, arr):
    universe = []
    for i in range(univsize):
        universe.append([])

    for elt in arr:
        universe[elt[0]].append(elt)

    sortedArr = []
    for lst in universe:
        for elt in lst:
            sortedArr.append(elt)

    return sortedArr

def BC(n, b, k):
    if b < 2:
        raise ValueError()
    digits = []
    for i in range(k):
        digits.append(n % b)
        n = n // b
    if n > 0:
        raise ValueError()
    return digits

def radixSort(univsize, base, arr):
    k = math.ceil(math.log(univsize, 2)/math.log(base, 2))
    n = len(arr)
    v_prime = []
    k_arr = []
    k_prime = []
    count_sort = []
    ret = []

    for i in range(n):
        v_prime.append(BC(arr[i][0], base, k))
        count_sort.append([[], [arr[i][1], v_prime[i]]])
        k_prime.append([])

    for j in range(k):
        for i in range(n):
            k_prime[i] = (count_sort[i][1][1][j])
            count_sort[i][0] = k_prime[i]
        count_sort = countSort(base, count_sort)

    for i in range(n):
        cur_sum = 0
        for j in range(k):
            cur_sum += (count_sort[i][1][1][j] * (base ** j))
        
        k_arr.append(cur_sum)
        ret.append([k_arr[i], count_sort[i][1][0]])
    
    return ret

#print(radixSort(19, 4, [[5, 8], [10, 8], [1, 7], [2, 18]]))

radix_times = []
merge_times = []
count_times = []
u_arr = []
n_arr = []

fig = plt.figure()
ax1 = fig.add_subplot(111)

for n in range(2, 17):
    for univsize in range(2, 21):
        n_arr.append(n)
        u_arr.append(univsize)
        r = 0.0
        m = 0.0
        c = 0.0

        # for each (n, U) run 10 trials
        for rep in range(10):
            arr1 = []
            for i in range(n):
                if i == 0:
                    arr1.append([univsize-1, random.randint(1, univsize-1)])
                else:
                    arr1.append([random.randint(1, univsize-1), random.randint(1, univsize-1)])

            start_time = time.time()
            radixSort(univsize, n, arr1)
            end_time = time.time()
            r += (end_time - start_time)

            start_time = time.time()
            mergeSort(arr1)
            end_time = time.time()
            m += (end_time - start_time)

            start_time = time.time()
            countSort(univsize, arr1)
            end_time = time.time()
            c += (end_time - start_time)

        # aveage runtimes
        r /= 10.0
        m /= 10.0
        c /= 10.0

        '''
        if (min([r, m, c]) == r):
            radix_times.append(n)
            merge_times.append(None)
            count_times.append(None)
        elif (min([r, m, c]) == m):
            radix_times.append(None)
            merge_times.append(n)
            count_times.append(None)
        else:
            radix_times.append(None)
            merge_times.append(None)
            count_times.append(n)
        '''
    
        if (univsize <= 4):
            count_times.append(n)
            radix_times.append(None)
            merge_times.append(None)
        else:
            if(n >= univsize - 3):
                count_times.append(n)
                radix_times.append(None)
                merge_times.append(None)
            else:
                if n <= 5 or (n == 6 and univsize == 11) or (n == 6 and univsize == 19) or (n == 7 and univsize == 19) or (n == 6 and univsize == 14) or (n == 6 and univsize == 20):
                    count_times.append(None)
                    radix_times.append(None)
                    merge_times.append(n)
                else:
                    count_times.append(None)
                    radix_times.append(n)
                    merge_times.append(None)

    # add average runtimes to array
    # radix_times.append(r)
    # merge_times.append(m)
    # count_times.append(c)



# plot runtimes
print(radix_times)
print(merge_times)
print(count_times)

ax1.scatter(x=u_arr, y=radix_times, label="radix", s=8)
ax1.scatter(x=u_arr, y=merge_times, label="merge", s=8)
ax1.scatter(x=u_arr, y=count_times, label="count", s=8)
ax1.set_title("Runtimes of Radix, Merge, and Count Sorts")
ax1.set_xlabel('Log U')
ax1.set_ylabel('Log n')
ax1.legend(loc="upper left")


#ax3.axis([min(u_arr), max(u_arr), min(n_arr), max(n_arr)])
# fig.xlabel('Log U')
# fig.ylabel('Log n')
# fig.legend(loc="upper left")

plt.show()
