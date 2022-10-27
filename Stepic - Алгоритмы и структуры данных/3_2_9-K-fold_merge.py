# https://stepik.org/lesson/12562/step/9
# 
# Дана последовательность целых чисел a[0..n-1] и натуральное число k, такое что для любых i, j: если j >= i + k, то a[i] <= a[j]. Требуется отсортировать последовательность. Последовательность может быть очень длинной. Время работы O(n * log(k)). Доп. память O(k).
# 
# Использовать слияние.
# 
# Sample Input:
#     20
#     0 3 1 2 4 7 6 8 9 5 13 12 10 11 14 16 17 19 15 18
#     10
# Sample Output:
#     0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19


from typing import Any, List, Tuple, Iterable, Callable

class HeapItem:
    def __init__(self, priority:int, value:Any=None) -> None:
        self.priority = priority
        self.value = value
    
class BinaryHeap:
    def __init__(self, ascending:bool=True) -> None:
        self.__body: List[HeapItem] = []
        self.ascending = ascending
    
    def __repr__(self) -> str:
        from os import linesep
        result = [f'{item.priority}:\t{item.value}' for item in self.__body]
        return linesep.join(result)

    def __iter__(self):
        result = BinaryHeap()
        result.__body = self.__body.copy()
        result.ascending = self.ascending
        return result

    def __next__(self):
        if self.fetch() is None:
            raise StopIteration()
        else:
            return self.extract()

    @property
    def __tail_index(self):
        return len(self.__body) - 1
    
    @staticmethod
    def __children_ids(index:int) -> Tuple[int, int]:
        return 2*index + 1, 2*index + 2
    
    @staticmethod
    def __parent_id(index:int) -> int:
        if index != 0:
            return (index - 1) // 2

    def __get(self, index:int=0) -> HeapItem:
        return self.__body[index]

    def __pop_tail(self) -> HeapItem:
        return self.__body.pop()

    def __append(self, item) -> None:
        self.__body.append(item)

    def __swap(self, index_1:int, index_2:int):
        self.__body[index_1], self.__body[index_2] = self.__body[index_2], self.__body[index_1]

    def __sift_up(self, item_index:int) -> None:
        parent_index = self.__parent_id(item_index)

        if parent_index is None:
            return

        item = self.__get(item_index)
        parent = self.__get(parent_index)
        
        
        if (item.priority > parent.priority) ^ self.ascending:
            self.__swap(item_index, parent_index)
            self.__sift_up(parent_index)
    
    def __sift_down(self, item_index:int) -> None:
        from math import inf

        indexes = {item_index: self.__get(item_index).priority}

        for child_index in self.__children_ids(item_index):
            try:
                child = self.__get(child_index)
                indexes[child_index] = child.priority
            except IndexError:
                pass
        
        if self.ascending:
            result_index = min(indexes, key=indexes.get)
        else:
            result_index = max(indexes, key=indexes.get)
        
        if result_index != item_index:
            self.__swap(item_index, result_index)
            self.__sift_down(result_index)

    def add(self, value:Any, priority:Any=None) -> None:
        if value is None:
            return
        if priority is None:
            priority = value
        elif callable(priority):
            priority = priority(value)

        try:
            priority > priority
        except TypeError:
            raise ValueError(f'Instances of {type(priority)}. Change priority settings.')

        item = HeapItem(priority=priority, value=value)
        self.__append(item)

        index = self.__tail_index
        self.__sift_up(index)

    def extract(self, index: int=0) -> Any:
        if index > self.__tail_index or index < 0:
            return

        self.__swap(index, self.__tail_index)
        item = self.__pop_tail()

        if self.__tail_index > 0:
            self.__sift_down(index)
        return item.value

    def fetch(self, index: int=0) -> Any:
        if index > self.__tail_index or index < 0:
            return
        
        item = self.__get(index)
        
        return item.value

    def from_iter(self, iterable_object: Iterable, priority: Any=None) -> None:
        if not hasattr(iterable_object, '__iter__'):
            raise ValueError(f'This iterable_object is not iterable')
        for item in iterable_object:
            self.add(value=item, priority=priority)
        return self


if __name__ == '__main__':
    n = input()
    list_ = [int(i) for i in input().split()]
    k = int(input())

    heap = BinaryHeap(ascending=True)
    for i in list_[:k]:
        heap.add(i)

    result = []  
    for i in list_[k:]:
        heap.add(i)
        result.append(heap.extract())

    result.extend(heap)

    print(*result)