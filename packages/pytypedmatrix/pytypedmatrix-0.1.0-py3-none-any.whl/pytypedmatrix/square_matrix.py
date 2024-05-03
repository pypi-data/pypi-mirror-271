from __future__ import annotations
from copy import deepcopy
from typing import Generic

from pytypedmatrix.generics import MT
from pytypedmatrix.exceptions import MatrixError


class SquareMatrix(Generic[MT]):
    """
    SquareMatrix class is an abstraction for square matrices.
    MT stands for Matrix Type and can be either int or float.

    Example:
        >>> matrix = SquareMatrix([[1, 2], [3, 4]])

        >>> print(matrix)
        SquareMatrix([[1, 2], [3, 4]])

        >>> matrix.dims
        (2, 2)

        >>> matrix.sum_all()
        10

        >>> matrix.sum_row(0)
        3

    TODO:
    - [ ] Implement a method to find the max element in the whole matrix
    - [ ] Implement a method to find the min element in the whole matrix
    - [ ] Implement a method to add matrices
    - [ ] Implement a method to subtract matrices
    - [ ] Implement a method to multiply matrices
    - [ ] Implement a method to transpose the matrix
    - [ ] Implement a method to find the determinant of the matrix
    - [ ] Implement a method to find the inverse of the matrix
    - [ ] Create tests for computation methods
    """

    def __init__(self, arr: list[list[MT]]) -> None:
        """Constructor for the SquareMatrix class.
        MT stands for Matrix Type and can be either int or float.

        Args:
            arr (list[list[MT]]): The 2D list representing the matrix. Type MT can be either int or float.

        Raises:
            MatrixError: If the matrix is not square or if the rows are not of the same length.
        """
        self.arr = arr
        rows, cols = self.dims
        if any([len(row) != cols for row in self.arr]):
            raise MatrixError("All rows must have the same length")
        elif rows == 0:
            raise MatrixError("Matrix must have at least one row")
        elif rows != cols:
            raise MatrixError("Matrix must be square")

    @staticmethod
    def fill(dims: tuple[int, int], value: MT) -> SquareMatrix[MT]:
        """Static method to create a square matrix of dimensions dims filled with value.

        Args:
            dims (tuple[int, int]): The dimensions of the matrix (rows, cols).
            value (MT): The value to fill the matrix with.

        Returns:
            SquareMatrix[MT]: The square matrix of dimensions dims filled with value.

        Example:
            >>> SquareMatrix.fill((2, 2), 0)
            SquareMatrix([[0, 0], [0, 0]])
        """
        arr = [[value for _ in range(dims[1])] for _ in range(dims[0])]
        return SquareMatrix[MT](arr)

    @property
    def dims(self) -> tuple[int, int]:
        """Property to get the dimensions of the matrix.

        Returns:
            tuple[int, int]: The dimensions of the matrix (rows, cols).

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.dims
            (2, 2)
        """
        return len(self.arr), len(self.arr[0])

    @property
    def rows(self) -> int:
        """Property to get the number of rows in the matrix.

        Returns:
            int: The number of rows in the matrix.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.rows
            2
        """
        return self.dims[0]

    @property
    def cols(self) -> int:
        """Property to get the number of columns in the matrix.

        Returns:
            int: The number of columns in the matrix.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.cols
            2
        """
        return self.dims[1]

    def __getitem__(self, key: int) -> list[MT]:
        """Get the row at the specified index.

        Args:
            key (int): The index of the row.

        Returns:
            list[MT]: The row at the specified index.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix[0]
            [1, 2]
        """
        return self.arr[key]

    def __setitem__(self, key: tuple[int, int], value: MT) -> None:
        """Set the value at the specified index.

        Args:
            key (tuple[int, int]): The index of the element (row, col).
            value (MT): The value to set at the specified index.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix[0][0] = 0
            >>> matrix
            SquareMatrix([[0, 2], [3, 4]])
        """
        self.arr[key[0]][key[1]] = value

    def get_col(self, col_index: int) -> list[MT]:
        """Get the column at the specified index.

        Args:
            col_index (int): The index of the column.

        Returns:
            list[MT]: The column at the specified index.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.get_col(0)
            [1, 3]
        """
        return [self.arr[i][col_index] for i in range(self.rows)]

    def sum_all(self) -> MT:
        """Calculate the sum of all elements in the matrix.

        Returns:
            MT: The sum of all elements in the matrix.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.sum_all()
            10
        """
        return sum([sum(row) for row in self.arr])

    def sum_row(self, row_index: int) -> MT:
        """Calculate the sum of elements in the specified row.

        Args:
            row_index (int): The index of the row.

        Returns:
            MT: The sum of elements in the specified row.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.sum_row(0)
            3
        """
        return sum(self.arr[row_index])

    def sum_col(self, col_index: int) -> MT:
        """Calculate the sum of elements in the specified column.

        Args:
            col_index (int): The index of the column.

        Returns:
            MT: The sum of elements in the specified column.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.sum_col(0)
            4
        """
        return sum(self.get_col(col_index))

    def min_row_el(self, row_index: int) -> MT:
        """Find the minimum element in the specified row.

        Args:
            row_index (int): The index of the row.

        Returns:
            MT: The minimum element in the specified row.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.min_row_el(0)
            1
        """
        return min(self.arr[row_index])

    def min_col_el(self, col_index: int) -> MT:
        """Find the minimum element in the specified column.

        Args:
            col_index (int): The index of the column.

        Returns:
            MT: The minimum element in the specified column.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.min_col_el(0)
            1
        """
        return min(self.get_col(col_index))

    def max_row_el(self, row_index: int) -> MT:
        """Find the maximum element in the specified row.

        Args:
            row_index (int): The index of the row.

        Returns:
            MT: The maximum element in the specified row.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.max_row_el(0)
            2
        """
        return max(self.arr[row_index])

    def max_col_el(self, col_index: int) -> MT:
        """Find the maximum element in the specified column.

        Args:
            col_index (int): The index of the column.

        Returns:
            MT: The maximum element in the specified column.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix.max_col_el(0)
            3
        """
        return max(self.get_col(col_index))

    def copy(self) -> SquareMatrix[MT]:
        """Create a deep copy of the matrix.

        Returns:
            SquareMatrix[MT]: A copy of the matrix.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> matrix_copy = matrix.copy()
            >>> matrix_copy
            SquareMatrix([[1, 2], [3, 4]])

            >>> matrix == matrix_copy
            False
        """
        return SquareMatrix(deepcopy(self.arr))

    def __str__(self) -> str:
        """Return a string representation of the matrix.

        Returns:
            str: A string representation of the matrix.

        Example:
            >>> matrix = SquareMatrix([[1, 2], [3, 4]])
            >>> print(matrix)
            SquareMatrix([[1, 2], [3, 4]])
        """
        return f"SquareMatrix({self.arr})"

    def print(self, title: str = "") -> None:
        """Void method to print the matrix.
        You'll most likely want to override this method in a subclass to customize the output.

        Args:
            title (str, optional): The title to display before printing the matrix. Defaults to "".
        """
        if title:
            print(f"--- {title} ---")
        for row in self.arr:
            print("[", end=" ")
            for element in row:
                print(round(float(element), 2), end=" ")
            print("]")
        print()
