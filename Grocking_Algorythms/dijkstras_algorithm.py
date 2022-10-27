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

class DijkstraSearch:
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

if __name__ == '__main__':
    DijkstraSearch(graph=examples[0]).find_way(start_pos='book',goal='piano')


