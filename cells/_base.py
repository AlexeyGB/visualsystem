""" Base classes and functions

"""


class BaseCell:
    """ Base class for cells

        Parameters
        ----------
        position : tuple, (row, column)
            The position of the cell in its layer

        input_ : numpy array
            Outputs of the previous level's cells

        n_iter : int, optional, default 0
            The number of iterations the cell has ran

        Attributes
        ----------
        position: tuple, (row, column)
            The position of the cell in its layer

        n_iter : int
            The number of iterations the cell has ran


    """

    def __init__(self, position, input_, n_iter=0):
        self.position = position
        self._input = input_
        self.n_iter = n_iter
