examples = [
        [   # max_size=4
            {'name': 'guitar', 'size': 1, 'value': 1500},
            {'name': 'player', 'size': 4, 'value': 3000},
            {'name': 'laptop', 'size': 3, 'value': 2000},
            {'name': 'iphone', 'size': 1, 'value': 2000},
            {'name': 'mp3_pl', 'size': 1, 'value': 1000},
        ],

        [   # max_size=6
            {'name': 'whater', 'size': 3, 'value': 10},
            {'name': 'book', 'size': 1, 'value': 3},
            {'name': 'food', 'size': 2, 'value': 9},
            {'name': 'coat', 'size': 2, 'value': 5},
            {'name': 'camera', 'size': 1, 'value': 6},
        ]
    ]


class DynamicSearch:
    

    def __init__(self, max_size: int):
        """
        Creates Dynamic programming table with <max_size> width
        """
        self.value_tab = []
        self.combination_tab = []
        self.max_size = max_size

    def _get_previous(self, size: int) -> tuple:
        """
        Return best value of 
        """
        if self.value_tab == [] or size < 1:
            return 0, []
        else:
            prev_value = self.value_tab[-1][size-1]
            prev_combination = self.combination_tab[-1][size-1]
            return prev_value, prev_combination

    def add_item(self, name:str, value:int, size:int, draw=False) -> None:
        """
        Add one row to current tab according to incoming data
        """
        value_list = []
        combination_list = []

        for current_size in range(1, self.max_size + 1):
            tmp_value, tmp_combination = self._get_previous(current_size - size)
            current_value = value + tmp_value
            current_combination = [name] + tmp_combination

            prev_value, prev_combination = self._get_previous(current_size)

            if size <= current_size and current_value > prev_value:
                value_list.append(current_value)
                combination_list.append(current_combination)
            else:
                value_list.append(prev_value)
                combination_list.append(prev_combination)
                
        self.value_tab.append(value_list)
        self.combination_tab.append(combination_list)

        if draw:
            for layer in self.value_tab:
                print(layer)

    def get_best(self) -> dict:
        """
        Return best option in current table
        """
        best_value, best_combination = self._get_previous(self.max_size)
        return {
            'value': best_value,
            'combination': best_combination,
        }

    def fill_tabs(self, items: list) -> dict:
        """
        Fill table according to items dict and return best option

        items = [
            {'name': <name_0>, 'size': <size_0>, 'value': <value_0>},
            {'name': <name_1>, 'size': <size_1>, 'value': <value_1>},
            ...
        ]
        
        """
        for item in items:
            self.add_item(**item)

        return self.get_best()


if __name__ == '__main__':
    DynamicSearch(max_size=4).fill_tabs(items=examples[0])