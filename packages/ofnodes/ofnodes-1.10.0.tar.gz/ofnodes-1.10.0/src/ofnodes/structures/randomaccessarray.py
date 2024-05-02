from ofnodes.sorting.mixins import BubbleSortMixin, ReverseOrderMixin
class RandomAccessArray(BubbleSortMixin, ReverseOrderMixin):
    """An array supporting random access with bubble sort and order reversal capabilities.

    This class represents an array that supports random access operations and also provides
    functionality for sorting elements using bubble sort algorithm and reversing the order
    of elements.

    Args:
        size (int): The size of the array.

    Attributes:
        _data (list): The underlying list to store array elements.

    Note:
        This class inherits from BubbleSortMixin and ReverseOrderMixin to leverage the
        bubble sort and order reversal functionalities.
    """
    def __init__(self, size):
        self._data = [None] * size

    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        self._data[index] = value

    def __len__(self):
        return len(self._data)

    def __dir__(self) -> list[str]:
        # Get the list of attributes and methods from the parent classes
        parent_dir = set(super().__dir__())
        # Filter out private attributes and methods
        excluded = {'_head', '_tail', '_target', 'reference_based_reverse_order', 'reference_based_bubble_sort','index_based_bubble_sort', 'index_based_reverse_order'}
        parent_dir = {attr for attr in parent_dir if attr not in excluded}
        # Return a sorted list of all attributes and methods
        return sorted(parent_dir)

    def __repr__(self):
        """Returns a string representation of the array.

        Returns:
            str: A string representation of the array.

        Example:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            >>> raarray
            RandomAccessArray([8, 2, 6, 4, 5])

        """
        return f"RandomAccessArray({self._data})"

    def __str__(self):
        """Returns a string representation of the array.

        Returns:
            str: A string representation of the array.

        Example:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            >>> str(raarray)
            '[8, 2, 6, 4, 5]'
        """
        return f"[{', '.join(str(item) for item in self._data)}]"

    def bubble_sort(self, ascending=True):
        """
        Examples:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]
            >>> raarray.bubble_sort()
            >>> raarray
            RandomAccessArray([2, 4, 5, 6, 8])
            >>> raarray.bubble_sort(ascending=False)
            >>> raarray
            RandomAccessArray([8, 6, 5, 4, 2])
        """
        return super().index_based_bubble_sort(ascending)

    def reverse_order(self):
        """
        Examples:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]
            >>> raarray.reverse_order()
            >>> raarray
            RandomAccessArray([5, 4, 6, 2, 8])"""
        return super().index_based_reverse_order()