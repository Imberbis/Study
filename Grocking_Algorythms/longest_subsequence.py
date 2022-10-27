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
        import matrix_2d
        table = matrix_2d.from_iter(
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


examples = [
    ['a', 'b', 'c'],
    'aec',
]

if __name__ == '__main__':
    longest_subsequence(
        sequence_1=examples[0],
        sequence_2=examples[1],
        successive=False,
        return_table=False
    )