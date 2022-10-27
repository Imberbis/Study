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