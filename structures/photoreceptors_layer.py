""" The models of layer of photoreceptor cells

"""

import numpy as np

from ..cells.photoreceptors import RodBinaryCell


class RodsBinaryLayer:
    """ Class for layer of binary rod cells

    Parameters
    ----------

    shape: tuple, (row, column)
        The shape of the layer

    data_source: object
        An object that gets new frame and has a method get_frame()
        that returns an np.array with this frame.
        Frame's pixels must have the values only 0 and 1.

    n_iter : int, optional, default 0
        The number of iterations the layer has ran


    Attributes
    ----------

    shape: tuple, (row, column)
        The shape of the layer

    n_iter: int
        The number of iterations the layer has ran
        
    cells : list
        2 dimensional array of cells

    input_: numpy array
        Layer's input at the last iteration
        Array's shape is equal to layer's shape

    response: numpy array
        Cells of the layer's current response
        Array's shape is equal to layer's shape

    Notes
    -----
    The functionality is moved to RodsBinaryLayer2.
    Stays here just for keeping some old code working.


    """

    def __init__(self, shape, data_source, n_iter=0):
        self.shape = shape
        self._data_source = data_source
        self.n_iter = n_iter
        self.input_ = None
        self.response = np.empty(self.shape, dtype=np.int8)
        self.cells = []
        self._create_cells()

    def _create_cells(self):

        for i in range(self.shape[0]):
            self.cells.append([])
            for j in range(self.shape[1]):
                self.cells[i].append(RodBinaryCell(position=(i, j),
                                                   n_iter=self.n_iter
                                                   )
                                     )

    def run(self):
        """ Perform one iteration

        """

        self.input_ = self._data_source.get_frame()

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.cells[i][j].run(self.input_)
                self.response[i][j] = self.cells[i][j].response

        self.n_iter += 1


class RodsBinaryLayer2:
    """ Class for layer of binary rod cells

    The layer is square

    Parameters
    ----------
    data_source: object
        An object that gets new frame and has an attribute frame
        that is an np.array with current frame.
        Frame's pixels must have the values only 0 and 1.

    n_iter : int, optional, default 0
        The number of iterations the layer has ran


    Attributes
    ----------

    shape: tuple, (row, column)
        The shape of the layer

    n_iter: int
        The number of iterations the layer has ran

    cells : list
        2 dimensional array of cells

    input_: numpy array
        Layer's input at the last iteration
        Array's shape is equal to layer's shape

    response: numpy array
        Cells of the layer's current response
        Array's shape is equal to layer's shape


    """

    def __init__(self, data_source, n_iter=0):
        self.shape = (
            data_source.field_size,
            data_source.field_size
        )
        self._data_source = data_source
        self.n_iter = n_iter
        self.input_ = None
        self.response = np.zeros(self.shape, dtype=np.uint8)
        self.cells = []
        self._create_cells()

    def _create_cells(self):

        for i in range(self.shape[0]):
            self.cells.append([])
            for j in range(self.shape[1]):
                self.cells[i].append(RodBinaryCell(position=(i, j),
                                                   n_iter=self.n_iter
                                                   )
                                     )

    def run(self):
        """ Perform one iteration

        """

        self.input_ = self._data_source.frame

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.cells[i][j].run(self.input_)
                self.response[i][j] = self.cells[i][j].response

        self.n_iter += 1