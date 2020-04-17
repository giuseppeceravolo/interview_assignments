"""
Write a function that finds the contiguous sub-array within an array (containing at least one number), read in input,
which has the largest sum.
The function should return both the sub-array and the corresponding sum.
Which is the complexity of your solution?
Can you do a solution with linear complexity?
"""


def find_contiguous_subarray_max_sum(array: "list of ints") -> ("list of ints", int):
    """Return the contiguous sub-array with the greatest sum within an input array, together with its sum.

    Args:
        array (list): a non-empty list of integer numbers.

    Returns:
        (list, int): a tuple consisting of the contiguous sub-array with the maximum sum and its sum.

    Raises:
        TypeError: If the input array is not a list.
        ValueError: If the input array is either an empty list or a list not containing integer numbers only.

    Notes:
        Time complexity is O(n) as we loop over every element of the input array only once.
        Space complexity is O(n) as we store a sub-array whose maximum length is the length of the array;
        also, we instantiate variables with single values.

    Examples:

        >>> array = [-2, 5]
        >>> find_contiguous_subarray_max_sum(array)
        ([5], 5)

        >>> array = [1, -3, 7, 0, -5, 9, -3]
        >>> find_contiguous_subarray_max_sum(array)
        ([7, 0, -5, 9], 11)

    """

    if not isinstance(array, list):
        raise TypeError("'array' must be a list.")
    if not (len(array) > 0 and all(isinstance(x, int) for x in array)):
        raise ValueError("'array' must be a non-empty list of integers only.")

    current_max = array[0]
    global_max = array[0]
    start = 0
    end = 0
    index_potential_maximum_subarray_starts = 0

    for i in range(1, len(array)):

        if array[i] > current_max + array[i]:
            current_max = array[i]
            index_potential_maximum_subarray_starts = i
        else:
            current_max += array[i]

        if current_max > global_max:
            global_max = current_max
            start = index_potential_maximum_subarray_starts
            end = i

    return array[start:end+1], global_max

"""
for array in arrays:
    subarray_max_sum, max_sum = find_contiguous_subarray_max_sum(array)
    print("input array: {}\nsub-array with maximum sum: {} whose sum is: {}".format(array, subarray_max_sum, max_sum))
    print("-"*70)

arrays = [
        # 7,                          # this will raise a TypeError
        # 'asd',                      # this will raise a TypeError
        # [],                         # this will raise a ValueError
        # ['1', 2],                   # this will raise a ValueError
        [-2, 5],  # ([5], 5)
        [1, -3, 7, 0, -5, 9, -3],  # ([7, 0, -5, 9], 11)
        [0, 0],  # ([0], 0)
        [-8, 0, 0, 0, 0, -2],  # ([0], 0)
        [8, 10, -6, -4, -7, 2],  # ([8, 10], 18)
        [-8, -4, -7, -2, 2, 7],  # ([2, 7], 9)
        [-4, 1, -10, 7, 9, 4],  # ([7, 9, 4], 20)
        [-3, 10, 2, -10, 3, -9],  # ([10, 2], 12)
        [10, 3, 8, -1, -2, 7],  # ([10, 3, 8, -1, -2, 7], 25)
        [5, 4, -7, -4, -1, 2],  # ([5, 4], 9)
        [10, 9, -9, -1, 3, 7],  # ([10, 9], 19)
        [-9, -4, 4, 0, 9, 10],  # ([4, 0, 9, 10], 23)
        [7, 2, -8, 1, -3, 10],  # ([10], 10)
        [4, 4, -5, -8, 8, 2],  # ([8, 2], 10)
        [-2, -3, -5, -7, -1],  # ([-1], -1)
        [-2, -3, -1, -5, -7],  # ([-1], -1)
    ]
subarray_expected_result = [
    ([5], 5),
    ([7, 0, -5, 9], 11),
    ([8], 8),
    ([0], 0),
    ([8, 10], 18),
    ([2, 7], 9),
    ([7, 9, 4], 20),
    ([10, 2], 12),
    ([10, 3, 8, -1, -2, 7], 25),
    ([5, 4], 9),
    ([10, 9], 19),
    ([4, 0, 9, 10], 23),
    ([10], 10),
    ([8, 2], 10),
    ([-1], -1),
    ([-1], -1),
]

for s, r in zip(arrays, subarray_expected_result):
    print("Input string to test:", s)
    print("Expected result for string:", r)
    print("Actual result for string:", find_contiguous_subarray_max_sum(s))
    print("Do they match? {}".format(r == find_contiguous_subarray_max_sum(s)))
    print("-" * 70)
"""