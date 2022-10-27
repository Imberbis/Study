# https://stepik.org/lesson/12556/step/7
# 
# Дан отсортированный массив различных целых чисел A[0..n-1] и массив целых чисел B[0..m-1].
# Для каждого элемента массива B[i] найдите минимальный индекс элемента массива A[k],
# ближайшего по значению к B[i].
# 
# Время работы поиска для каждого элемента B[i]: O(log(k)).
# 
# Подсказка: Обратите внимание, что время работы должно зависеть от индекса ответа - k. Для достижения такой асимптотики предлагается для начала найти отрезок вида [2^p, 2^(p+1)], 
# содержащий искомую точку, а уже затем на нём выполнять традиционный бин. поиск.
# 
# Sample Input:
#     3
#     10 20 30
#     3
#     9 15 35
# 
# Sample Output:
#     0 0 2   
# 

def bin_search_closest(list_: list, value: int):
    """
    Performs a search on a sorted array (<list_>). 
    Returns position of the number with the closest value.
    """
    if len(list_) ==  1:
        return 0

    middle_position = len(list_) // 2

    right_diff = abs(list_[middle_position] - value)
    left_diff = abs(list_[middle_position - 1] - value)

    if left_diff <= right_diff:
        return bin_search_closest(list_[:middle_position], value)
    else: 
        return middle_position + bin_search_closest(list_[middle_position:], value)


class IndexedList(list):
    """
    Custom list that takes sorted list and creates indexes for search improvement

    Methods self.search performs a search on self. 
    Returns position of the number with the closest value.
    """
    def __init__(self, *args, **kwargs):
        super(IndexedList, self).__init__(*args, **kwargs)
        self.__create_index()

    @staticmethod
    def __bin_search_closest(list_: list, value: int):
        """
        Binary_search_closest function to use in improved search.

        Performs a search on a sorted array (<list_>). 
        Returns position of the number with the closest value.
        """
        if len(list_) ==  1:
            return 0
        middle_position = len(list_) // 2

        right_diff = abs(list_[middle_position] - value)
        left_diff = abs(list_[middle_position - 1] - value)

        if left_diff <= right_diff:
            return IndexedList.__bin_search_closest(list_[:middle_position], value)
        else: 
            return middle_position + IndexedList.__bin_search_closest(list_[middle_position:], value)

    def __create_index(self):
        """
        Creates index
        """
        from math import log2
        self.__max_value = self[-1]
        _max_power = int(log2(self.__max_value)) + 1
        self.__search_index = [IndexedList.__bin_search_closest(self, 2**i) for i in range(_max_power + 1)]

    def search(self, value):
        """
        Performs a search on self using index to improve perfomance.
        """
        from math import log2
        if value > self.__max_value:
            return len(self) - 1
        elif value == 0:
            return 0
        else:
            power = int(log2(value))
            area_of_search = slice(self.__search_index[power], self.__search_index[power + 1] + 1)
            return self.__search_index[power] + IndexedList.__bin_search_closest(list_A[area_of_search], value=value)       


if __name__ == '__main__':
    input()
    list_A = IndexedList(map(int, input().split()))
    input()
    list_B = list(map(int, input().split()))

    result = [list_A.search(item) for item in list_B]
    print(*result)