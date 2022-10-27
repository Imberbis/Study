# Not a part of book's materials. I used it for some algorithms as 2d array with visualisation.

def from_iter(iter_1, iter_2, default_value=None):
    return Matrix_2d(
            x_len=len(iter_1),
            y_len=len(iter_2),
            x_index=list(iter_1),
            y_index=list(iter_2),
            default_value=default_value
        )


class Matrix_2d:
    def __init__(self, x_len:int, y_len:int, default_value=None, x_index=None, y_index=None):
        self.shape = (x_len, y_len)
        self.table = [[default_value for y in range(y_len)] for x in range(x_len)]
        self.x_index = x_index
        self.y_index = y_index

    def __getitem__(self, x):
        return self.__get_column(x)

    def __get_row(self, n):
        return [row[n] for row in self.table]
    
    def __get_column(self, n):
        return self.table[n]
    
    def __repr__(self) -> str:
        def _column_width(column: list) -> int:
            return max([len(str(item)) for item in column])

        def _width_list() -> list:
            width_list = []
            if self.y_index:
                width_list.append(_column_width(self.y_index))
            for column_number in range(self.shape[0]):
                column = self.__get_column(column_number)
                column_width = _column_width(column)
                width_list.append(column_width)
            return width_list 

        def _draw_row(n:int, width_list:list, min_width:int=2):
            if n == 'index':
                row = self.x_index[:self.shape[0]]
                if self.y_index:
                    row = [''] + row
            else:
                row = self.__get_row(n)
                if self.y_index:
                    row = [self.y_index[n]] + row

            default_space = ' ' * min_width

            return default_space.join([
                str(item).rjust(width_list[position]) for position, item in enumerate(row)
                ])

        from os import linesep
        width_list = _width_list()

        result = []
        if self.x_index:
            result.append(_draw_row('index', width_list))
        for n in range(self.shape[1]):
            result.append(_draw_row(n, width_list))

        result = linesep.join(result)
        return result
