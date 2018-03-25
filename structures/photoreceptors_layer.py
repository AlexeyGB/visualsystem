""" The models of layer of photoreceptor cells

"""

from copy import deepcopy

import numpy as np

from ..cells.photoreceptors import RodBinary


class RodsBinaryLayer:
    """ Class for layer of binary rod cells

    Parameters
    ----------

    shape: tuple, (row, column)
        The shape of the layer

    data_source: object
        An object that gets new frame and has a method get_frame()
        that returns an np.array with this frame


    Attributes
    ----------

    shape: tuple, (row, column)
        The shape of the layer

    n_iter: int
        The number of iterations the layer has ran


    """

    def __init__(self, shape, data_source):
        self.shape = shape
        self._data_source = data_source
        self.n_iter = 0
        self._input = None
        self._response = np.empty(self.shape, dtype=np.int8)
        self._create_cells()

    def _create_cells(self):
        self._cells = []

        for i in range(self.shape[0]):
            self._cells.append([])
            for j in range(self.shape[1]):
                self._cells[i].append(RodBinary(position=(i, j)))

    def run(self):
        """ Perform one iteration

        """

        self._input = deepcopy(self._data_source.get_frame())

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self._cells[i][j].run(self._input)
                self._response[i][j] = self._cells[i][j].get_response()

        self.n_iter += 1

    def get_response(self):
        """
        Getting layer's current response

        Returns
        -------
        response: numpy array
            Array's shape is equal to layer's shape

        """

        response = self._response
        return response

    def get_input(self):
        """
        Getting layer's current input

        Returns
        -------
        input_: numpy array
            Array's shape is equal to layer's shape

        """

        input_ = self._input
        return input_

    def get_cells(self):
        cells = self._cells
        return cells
