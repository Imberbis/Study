# https://stepik.org/lesson/12559/step/8
# 
# Дан фрагмент последовательности скобок, состоящей из символов (){}[].
# Требуется определить, возможно ли продолжить фрагмент в обе стороны, получив корректную последовательность.
# Если возможно - выведите минимальную корректную последовательность, иначе - напечатайте "IMPOSSIBLE".
# Максимальная длина строки 10^6 символов.
# 
# Sample Input 1:
#     }[[([{[]}
# 
# Sample Output 1:
#     {}[[([{[]}])]]
# 
# Sample Input 2:
#     {][[[[{}[]
# 
# Sample Output 2:
#     IMPOSSIBLE
# 

class BracketCheck:
    character_catalog = {
        # Character dictionary to use in some funcs. Makes system scalable.
        '{': {'self': '{', 'direction': 'open', 'opposite': '}'},
        '}': {'self': '}', 'direction': 'close', 'opposite': '{'},
        '(': {'self': '(', 'direction': 'open', 'opposite': ')'},
        ')': {'self': ')', 'direction': 'close', 'opposite': '('},
        '[': {'self': '[', 'direction': 'open', 'opposite': ']'},
        ']': {'self': ']', 'direction': 'close', 'opposite': '['},
    }
    def __init__(self) -> None:
        self.__body = []
        self.__close_queue = []
        self.__open_queue = []

    def __repr__(self) -> str:
        """
        Some info about the queues in convenient representation.
        
        """
        left_queue = ''.join(self.__close_queue) if self.__close_queue else 'empty'
        right_queue = ''.join(self.__open_queue) if self.__open_queue else 'empty'
        return f"{left_queue} + {right_queue}"

    @staticmethod
    def __opposite(char) -> str:
        """
        Returns opposite to <char> according to BracketCheck character catalog.
        """
        return BracketCheck.character_catalog[char]['opposite']
    
    @staticmethod
    def __direction(char) -> str:
        """
        Returns direction of <char> according to BracketCheck character catalog.
        """
        return BracketCheck.character_catalog[char]['direction']

    @property
    def __current_opposite(self) -> dict:
        """
        Returns direction of last character in forward queue.
        """
        current_char = self.__open_queue[-1]
        return self.__opposite(current_char)
    
    def add(self, char: str) -> None:
        """
        Adds a character to its memory. Returns ValueErroe in case <char> can not be written here.
        """
        if self.__direction(char) == 'open':
            self.__open_queue.append(char)
            self.__body.append(char)
        elif self.__open_queue == []:
            self.__close_queue.append(char)
            self.__body.append(char)
        elif self.__current_opposite == char:
            self.__open_queue.pop()
            self.__body.append(char)
        else:
            raise ValueError(f'Incorrect input. Can`t add this symbol.')

    def add_string(self, string: str) -> None:
        """
        Adds a character to its memory. Returns ValueErroe if any character of string can not be written here.
        """
        for position, char in enumerate(string):
            try:
                self.add(char)
            except ValueError as E:
                raise ValueError(f'Char: {char}, Position: {position} \n {E}')

    def finish_sequence(self) -> str:
        """
        Retiurns the inserted sequence with additional brackets to comply with the rules of bracket writing.
        """
        left_side = [self.__opposite(char) for char in self.__close_queue[::-1]]
        right_side = [self.__opposite(char) for char in self.__open_queue][::-1]
        return ''.join(left_side + self.__body + right_side)


NEGATIVE_ANSWER = 'IMPOSSIBLE'

if __name__ == '__main__':
    bc = BracketCheck()
    
    string = input()

    try:
        bc.add_string(string)
        print(bc.finish_sequence())

    except ValueError:
        print(NEGATIVE_ANSWER)