# https://stepik.org/lesson/12556/step/3
# 
# Даны два массива целых чисел одинаковой длины A[0..n-1] и B[0..n−1].
# Необходимо найти первую пару индексов i_0 и j_0, i_0 ≤ j_0, 
# такую что A[i_0] + B[j_0] = max{A[i] + B[j], где 0 <= i < n, 0 <= j < n
# 
# Время работы – O(n).
# Ограничения: 1≤n≤100000,0≤A[i]≤100000,0≤B[i]≤100000  для любого i.
# 
# Sample Input:
#   4
#   4 -8 6 0
#   -10 3 1 1
# 
# Sample Output:
#   0 1
# 

def main(list_A: list, list_B: list) -> tuple:
    from math import inf

    maximums = [None for i in list_B]
    positions = [None for i in list_B]

    prev_max = -inf
    prev_i = None
    for i in range(len(list_B))[::-1]:
        if list_B[i] >= prev_max:
            prev_max = list_B[i]
            prev_i = i

        maximums[i] = prev_max
        positions[i] = prev_i

    max_value = -inf
    max_index_A = None
    max_index_B = None
    for i in range(len(list_A)):
        if list_A[i] + maximums[i] > max_value:
            max_value = list_A[i] + maximums[i]
            max_index_A = i
            max_index_B = positions[i]

    return max_index_A, max_index_B

if __name__ == "__main__":
    _ = input()
    list_A = list(map(int, input().split()))
    list_B = list(map(int, input().split()))

    print(*main(list_A, list_B))