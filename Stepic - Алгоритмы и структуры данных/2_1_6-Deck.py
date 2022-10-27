# https://stepik.org/lesson/12559/step/7
# 
# Реализуйте дек с динамическим зацикленным буфером.
# Для тестирования дека на вход подаются команды.
# В первой строке количество команд. Затем в каждой строке записана одна команда. 
# Каждая команда задаётся как 2 целых числа: a b.
# 
# a = 1 - push front,
# a = 2 - pop front,
# a = 3 - push back, 
# a = 4 - pop back.
# 
# Если дана команда pop*, то число b - ожидаемое значение. Если команда pop вызвана для пустой структуры данных, то ожидается “-1”.
# Требуется напечатать YES, если все ожидаемые значения совпали. Иначе, если хотя бы одно ожидание не оправдалось, то напечатать NO.
# 
# Sample Input:
#     5
#     1 44
#     3 50
#     2 44
#     2 50
#     2 -1
# 
# Sample Output:
#     YES

class Deck:
    def __init__(self, max_size: int) -> None:
        self.__body = [None for _ in range(max_size)]
        self.max_size = max_size
        self.size = 0
        self.__head_pointer = 0
        self.__tail_pointer = 0

    def _count_pointer(self, pointer: int, step: int) -> int:
        """
        Counts new value of pointer. Used to avoid IndexError.
        
        """
        return (pointer + step + self.max_size) % self.max_size

    def _move_head(self, step: int) -> None:
        """
        Adds <step> to head_pointer.
        
        """
        self.__head_pointer = self._count_pointer(self.__head_pointer, step)
    
    def _move_tail(self, step: int) -> None:
        """
        Adds <step> to tail_pointer.
        
        """
        self.__tail_pointer = self._count_pointer(self.__tail_pointer, step)

    def push_front(self, value):
        """
        Adds element to head and moves head_pointer.
        
        """
        if self.size == self.max_size:
            raise ValueError('Too many items: deck overflow.')
        if self.size > 0:
            self._move_head(-1)
        self.size += 1
        self.__body[self.__head_pointer] = value
        
    def push_back(self, value):
        """
        Adds element to head and moves tail_pointer.
        
        """
        if self.size == self.max_size:
            raise ValueError('Too many items: deck overflow.')
        if self.size > 0:
            self._move_tail(1)
        self.size += 1
        self.__body[self.__tail_pointer] = value

    def pop_front(self, *args):
        """
        Removes element from head and moves head_pointer. Returns removed element.
        
        """
        if self.size == 0:
            return -1

        value = self.__body[self.__head_pointer]
        if self.size > 1:
            self._move_head(1)
        self.size -= 1
        return value

    def pop_back(self, *args):
        """
        Removes element from head and moves tail_pointer. Returns removed element.
        
        """
        if self.size == 0:
            return -1

        value = self.__body[self.__tail_pointer]
        if self.size > 1:
            self._move_tail(-1)
        self.size -= 1
        return value
    
    def __repr__(self):
        """
        Some info about the deck in convenient representation.
        
        """
        if self.size == 0:
            result = ''
        elif self.__head_pointer <= self.__tail_pointer:
            result = self.__body[self.__head_pointer:self.__tail_pointer + 1]
        else:
            result = self.__body[self.__head_pointer:] + self.__body[:self.__tail_pointer + 1]
        return f'{self.size}/{self.max_size} | {result}'


if __name__ == '__main__':
    deck = Deck(50)
    interface = {
        1: deck.push_front,
        2: deck.pop_front,
        3: deck.push_back,
        4: deck.pop_back,
    }

    result = True

    n = int(input())
    for _ in range(n):
        command, value = [int(i) for i in input().split()]
        response = interface[command](value)
        if command in (2, 4):
            result = result and response == value

    if result:
        print('YES')
    else:
        print('NO')
