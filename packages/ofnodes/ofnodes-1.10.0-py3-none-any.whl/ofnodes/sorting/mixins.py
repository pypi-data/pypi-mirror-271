from ofnodes.nodes.singlynode import SinglyNode

class BubbleSortMixin:
    """Mixin class providing bubble sort functionality for linked node structures."""
    def reference_based_bubble_sort(self, ascending=True):
        """Sorts the nodes of the singly linked data structure.

        Args:
            ascending (bool, optional): Specifies whether to sort the elements in ascending order (default) or descending order.

        Returns:
            None: This method modifies the original linked list in place.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.reference_based_bubble_sort()
            >>> sllist
            SinglyLinkedList([2, 4, 5, 6, 8])
            >>> sllist.reference_based_bubble_sort(ascending=False)
            >>> sllist
            SinglyLinkedList([8, 6, 5, 4, 2])

        Notes:
            - The comparison operation (`>`) is used for elements. For non-numeric data types,
            ensure that the `__gt__` method is defined appropriately for comparison.
            - Time Complexity:
                - Best Case: O(n), when the list is already sorted.
                - Worst Case: O(n^2), when the list is in reverse order.
                - Average Case: O(n^2).
        """
        if 'head' not in dir(self):
            raise TypeError("reference_based_bubble_sort can only be used on reference-based data structures like linked lists.")
        if not self.head or not self.head.next:  # it's a zero node or one node list
            raise ValueError("Cannot sort an empty linked list.")
        swapped = True
        while swapped:
            swapped = False
            # Complete ascending sort
            current = self._head
            while current.next:
                if current._data > current.next._data:
                    current._data, current.next._data = current.next._data, current._data
                    swapped = True
                current = current.next
        if not ascending:  # it's descending
            self.reverse_order()

    def index_based_bubble_sort(self, ascending= True):
        """
        Examples:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]
            >>> raarray.index_based_bubble_sort()
            >>> raarray
            RandomAccessArray([2, 4, 5, 6, 8])
            >>> raarray.index_based_bubble_sort(ascending=False)
            >>> raarray
            RandomAccessArray([8, 6, 5, 4, 2])
        """
        if '__getitem__' not in dir(self):
            raise TypeError("index_based_bubble_sort can only be used on data structures that support index-based access.")
        n = len(self)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1): # (5 - 0 - 1)
                if self[j] > self[j + 1]:
                    self[j], self[j + 1] = self[j + 1], self[j]
                    already_sorted = False
            if already_sorted:
                break
        if not ascending:  #it's descending
            self.index_based_reverse_order()

class ReverseOrderMixin:
    """Mixin class supporting node order reversal for linked node structures."""
    def reference_based_reverse_order(self):
        """Reverses the order of elements in the singly linked data structure.

        Returns:
            None: This method modifies the original linked list in place.

        Examples:
            >>> sllist = SinglyLinkedList([8, 2, 6, 4, 5])
            >>> sllist.reference_based_reverse_order()
            >>> sllist
            SinglyLinkedList([5, 4, 6, 2, 8])

        Notes:
            - Time Complexity: O(n), where n is the number of elements in the linked list.
        """
        if 'head' not in dir(self):
            raise TypeError("reference_based_reverse_order can only be used on reference-based data structures like linked lists.")
        if not self.head or not self.head.next:  # it's a zero node or one node list
            raise ValueError("Cannot reverse an empty linked list.")
        ## it's more than one node list
        # set the head
        self.head = SinglyNode(self.tail.data)  # trigger the setter
        self.remove_tail()  # remove the node you moved data from
        # complete node order reversal
        current = self._head
        while current is not self.tail:  # or while head_to_tail.next is not None
            node = SinglyNode(self._tail.data)
            node._next, current._next = current._next, node
            self.remove_tail()
            current = current.next

    def index_based_reverse_order(self):
        """Reverses the order of elements in the index-based data structure.

        Returns:
            None: This method modifies the original data structure in place.

        Examples:
            >>> raarray = RandomAccessArray(5)
            >>> [raarray.__setitem__(i, val) for i, val in enumerate([8, 2, 6, 4, 5])]
            [None, None, None, None, None]
            >>> raarray.index_based_reverse_order()
            >>> raarray
            RandomAccessArray([5, 4, 6, 2, 8])

        Notes:
            - Time Complexity: O(n), where n is the number of elements in the data structure.
        """
        if '__getitem__' not in dir(self):
            raise TypeError("index_based_reverse_order can only be used on data structures that support index-based access.")
        n = len(self)
        for i in range(n // 2):
            # Swap elements symmetrically across the middle
            self[i], self[n - i - 1] = self[n - i - 1], self[i]