# https://stepik.org/lesson/12562/step/7
# 
# На числовой прямой окрасили N отрезков. Известны координаты левого и правого концов каждого отрезка (Li и Ri). Найти сумму длин частей числовой прямой, окрашенных ровно в один слой.
# 
# Для сортировки реализуйте сортировку слиянием.
# 
# Sample Input:
#     3
#     1 4
#     7 8
#     2 5
# 
# Sample Output:
#     3 


def merge_sort(list_: list) -> list:
    if len(list_) < 2:
        return list_

    sep = len(list_) // 2
    sub_list_1 = merge_sort(list_[:sep])
    sub_list_2 = merge_sort(list_[sep:])

    result = []
    while sub_list_1 or sub_list_2:
        if not sub_list_1:
            result.extend(sub_list_2)
            break
        elif not sub_list_2:
            result.extend(sub_list_1)
            break
        
        if sub_list_1[0] <= sub_list_2[0]:
            result.append(sub_list_1.pop(0))

        elif sub_list_1[0] > sub_list_2[0]:
            result.append(sub_list_2.pop(0))
    return result


if __name__ == '__main__':
    n = int(input())
    list_ = []
    for _ in range(n):
        x, y = [int(i) for i in input().split()]
        list_.append((x, 1))
        list_.append((y, -1))
    
    # list_ = l
    list_ = merge_sort(list_)

    previous_coordinate, layer_count = list_[0]
    length = 0
    for coordinate, status in list_[1:]:
        if layer_count == 1:
            length += coordinate - previous_coordinate
        layer_count += status
        previous_coordinate = coordinate
    print(length)