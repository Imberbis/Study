# https://stepik.org/lesson/12560/step/7
# 
# Жадина.
# 
# Вовочка ест фрукты из бабушкиной корзины. В корзине лежат фрукты разной массы. Вовочка может поднять не более K грамм. Каждый фрукт весит не более K грамм. За раз он выбирает несколько самых тяжелых фруктов, которые может поднять одновременно, откусывает от каждого половину и кладет огрызки обратно в корзину. Если фрукт весит нечетное число грамм, он откусывает большую половину. Фрукт массы 1гр он съедает полностью.
# Определить за сколько подходов Вовочка съест все фрукты в корзине.
# 
# Напишите свой класс кучи, реализующий очередь с приоритетом.
# 
# Формат входных данных. Вначале вводится n - количество фруктов и строка с целочисленными массами фруктов через пробел. Затем в отдельной строке K - "грузоподъемность".
# Формат выходных данных. Неотрицательное число - количество подходов к корзине.
# 
# Sample Input:
#     3
#     1 2 2
#     2
# 
# Sample Output:
#     4


# Binary heap stuff

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
        
# Task abstractions    
def _put_in_basket(fruits: int, basket: BinaryHeap = None) -> None:
    """
    Adds items from <fruits> to the <basket>. Creates a new basket if no basket given.
    Returns the <basket>.
    """
    if basket is None:
        basket = BinaryHeap(ascending=False)

    for fruit in fruits:
        basket.add(value=fruit)

    return basket


def _grab(basket: BinaryHeap, max_weight: int) -> list:
    """
    Takes some items from the basket according to the max_weight.
    Returns list of taken items.
    """
    handful = []
    handful_weight = 0

    while basket.fetch():
        if basket.fetch() + handful_weight <= max_weight:
            new_fruit = basket.extract()
            handful.append(new_fruit)
            handful_weight += new_fruit
        else:
            break

    return handful

def _eat_handful(handful: list) -> list:
    """
    Changes the size of given items according to the rules of fruit biting.
    Returns list of changed item sizes.
    """
    def _bite(size: int) -> int:
        return size // 2

    return [_bite(fruit) for fruit in handful if _bite(fruit) > 0]


def how_long_can_you_eat_this(fruits: list, max_weight: int) -> int:
    """
    Eat all the fruits from <fruits>. Counts number of iterrations of grabbing and biting.
    Returns the number of iterrations.
    """
    iterration_counter = 0

    basket = _put_in_basket(fruits)

    while basket.fetch():
        handful = _grab(basket, max_weight)

        if not handful:
            raise StopIteration(f'Something`s wrong here. Fruits: {fruits}. Max_weight: {max_weight}')
            
        handful = _eat_handful(handful)
        _put_in_basket(handful, basket)

        iterration_counter += 1
    
    return iterration_counter



if __name__ == '__main__':
    n = int(input())
    fruits = [int(i) for i in input().split()]
    k = int(input())

    print(how_long_can_you_eat_this(fruits=fruits, max_weight=k))