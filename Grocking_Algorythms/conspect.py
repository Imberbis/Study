# <Recursion funcs>
def recursive_max(list_):
    """
    Recursevely count max of list values

    list_ : list[int | float]
    """
    if list_ == []:
        return None
    next_max = recursive_max(list_[1:])
    if next_max is not None and next_max > list_[0]:
        return next_max
    else: 
        return list_[0]

def recursive_quicksort(list_: list[int], ascending=True):
    """
    Recursevely sort list (ascending)

    list_ : list[int | float]
    """
    if len(list_) < 2:
        return list_
    base = list_[0]
    left_list = [i for i in list_[1:] if i <= base]
    right_list = [i for i in list_[1:] if i > base]
    result = recursive_quicksort(left_list) + [base] + recursive_quicksort(right_list)
    if ascending:
        return result
    else:
        return result[::-1]
# </Recursion funcs>

# <Dijkstra's algorithm>
class DijkstraSearch:
    examples = [
        {
            'book':     {'poster': 0,   'disc': 5},
            'poster':   {'guitar': 30,  'drum': 35},
            'disc':     {'guitar': 15,  'drum': 20},
            'guitar':   {'piano': 20},
            'drum':     {'piano': 10},
            'piano':    {},
        },

        {
            'start': {'A': 5, 'B': 2},
            'A': {'C': 4, 'D': 2},
            'B': {'A': 8, 'D': 7},
            'C': {'D': 6, 'finish': 3},
            'D': {'finish': 1},
            'finish': {}
        }
    ]

    def __init__(self, graph: dict) -> None:
        """
        Take dict description of graph

        graph = {
            <item_1>: {<itemname>: <connection_cost>, <itemname>: <connection_cost>, ...}
            <item_2>: {<itemname>: <connection_cost>, <itemname>: <connection_cost>, ...}
            ...
        }
        """
        self.items = graph
        
    def _update_costs(self, current_pos: str) -> None:
        """
        Update costs in self.costs according to values in self.items[current_pos]
        """
        for node, cost in self.items[current_pos].items():
            cost += self.costs[current_pos]
            if self.costs[node] > cost:
                self.costs[node] = cost
                self.parents[node] = current_pos


    def _find_new(self):
        """
        Choose item for next iterration of search
        """
        from math import inf
        slice_ = {key: value for key, value in self.costs.items() if key not in self.checked}
        if len(slice_) == 0:
            return None
        new = min(slice_, key=slice_.get)
        if self.costs[new] < inf:
            return new


    def find_way(self, start_pos: str, goal: str, draw_results=False):
        """
        Pathfinder from start_pos to goal

        Var:
            start_pos: name of starting item,
            goal: name of item to find
        """
        from math import inf
        self.checked = set()
        self.parents = {key: None for key in self.items}
        self.costs = {key: inf if key!= start_pos else 0 for key in self.items}

        while True:
            current_pos = self._find_new()
            if current_pos is None:
                break
            else:
                self._update_costs(current_pos)
                self.checked.add(current_pos)

        current_pos = goal
        if self.parents[current_pos] or start_pos==goal:
            chain = []
            while self.parents[current_pos]:
                chain.append(current_pos)
                current_pos = self.parents[current_pos]
            chain.append(current_pos)
            return {
                'Way': '->'.join(chain[::-1]),
                'Cost': self.costs[goal]
            }
        else:
            return('No way')


# DijkstraSearch(graph=DijkstraSearch.examples[0]).find_way(start_pos='book',goal='piano')

# </Dijkstra's algorithm>

# <DynamicSearch>
class DynamicSearch:
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

# DynamicSearch(max_size=4).fill_tabs(items=DynamicSearch.examples[0])

# </DynamicSearch>


# <GreatestSubsequence>
def longest_subsequence(sequence_1, sequence_2, successive:bool=False, return_table:bool=False):
    """
    This func finds longest subsequence of two sequences. 
    It works nice with any combinations of list, touple and string. (Might work with other subscriptable collections)

    Works both with successive and non-successive subsequence.

    Arguments:
        sequence_1: list | touple | string | <other_subscriptable_collection>
        sequence_2: list | touple | string | <other_subscriptable_collection>
    Returns:
        result | (result, table) # if return_table=False

    Vars:
        result: dict = {
                'length': <length of greatest substring>,
                'substring': <greatest substring>,
            }

        table: Matrix_2d | list[list] 

    """
    try:
        # This is custom 2D matrix. Just list of lists but more handsome (has indexes and prints as normal flat table). 
        # If you don't have one it's ok. The func will generate normal 2D list.
        import Matrix_2d
        table = Matrix_2d.from_iter(
            iter_1=sequence_1,
            iter_2=sequence_2,
            default_value=None
        )
    except ModuleNotFoundError:
        table = [[None for y in range(len(sequence_2))] for x in range(len(sequence_1))]

    sequence_1_binary_mask = [False for i in range(len(sequence_1))]
    sequence_2_binary_mask = [False for i in range(len(sequence_2))]
            
    len_x = len(sequence_1)
    len_y = len(sequence_2)

    def _check(x: int, y: int):
        if x < 0 or y < 0:
            return 0
        elif table[x][y]:
            return table[x][y]
            
        elif sequence_1[x] != sequence_2[y]:
            if successive:
                return 0
            else:
                return _check(x-1, y-1)

        else:
            table[x][y] = 1 + _check(x-1, y-1)
            sequence_1_binary_mask[x] = True
            sequence_2_binary_mask[y] = True
            return table[x][y]
                
    max_length = 0
    x_max = y_max = None
    for x in range(len_x):
        for y in range(len_y):
            value = _check(x, y)
            if value > max_length:
                max_length = value
                x_max, y_max = x, y
            table[x][y] = value

    if successive:
        subsequence = sequence_1[x_max + 1 - max_length : x_max + 1]
    else:
        subsequence = [item for item, status in zip(sequence_1, sequence_1_binary_mask) if status]

    report = {'length': max_length, 'subsequence': subsequence}
    
    # Set return_table=True if you want to get table of calculations.
    if return_table:
        return report, table
    else:
        return report

# sequence_1 = ['a', 'b', 'c']
# sequence_2 = 'aec'
# longest_subsequence(
#     sequence_1=sequence_1,
#     sequence_2=sequence_2,
#     successive=False,
#     return_table=False
# )
# </GreatestSubsequence>