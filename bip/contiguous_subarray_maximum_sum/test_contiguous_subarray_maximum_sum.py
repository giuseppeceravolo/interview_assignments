import unittest
import contiguous_subarray_maximum_sum as csms


class TestLargestSubarray(unittest.TestCase):

    arrays = [
        [-2, 5],
        [1, -3, 7, 0, -5, 9, -3],
        [0, 0],
        [-8, 0, 0, 0, 0, -2],
        [8, 10, -6, -4, -7, 2],
        [-8, -4, -7, -2, 2, 7],
        [-4, 1, -10, 7, 9, 4],
        [-3, 10, 2, -10, 3, -9],
        [10, 3, 8, -1, -2, 7],
        [5, 4, -7, -4, -1, 2],
        [10, 9, -9, -1, 3, 7],
        [-9, -4, 4, 0, 9, 10],
        [7, 2, -8, 1, -3, 10],
        [4, 4, -5, -8, 8, 2],
        [-2, -3, -5, -7, -1],
        [-2, -3, -1, -5, -7],
    ]

    subarray_expected_result = [
        ([5], 5),
        ([7, 0, -5, 9], 11),
        ([0], 0),
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

    def test_find_contiguous_subarray_max_sum(self):
        for s, r in zip(self.arrays, self.subarray_expected_result):
            result = csms.find_contiguous_subarray_max_sum(s)
            self.assertEqual(result, r)

if __name__ == '__main__':
    unittest.main()
