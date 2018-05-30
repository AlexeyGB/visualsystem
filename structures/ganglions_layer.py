""" The models of layer of ganglion cells

"""

from copy import deepcopy

import numpy as np

from ..cells.ganglion import GanglionBinaryCell
from ._base import get_csarf


class GanglionsBinaryLayer:
    """ Class for layer of binary ganglion cells
        Provides two configurations: on-center and off-center cells.

    Parameters
    ----------

    previous_layer : object
        An object of a rod's layer

    receptive_field_shape : tuple, {center_radius, surround_radius}

    center_surround_tolerance : {'constant', 'linear', 'elliptical'},
                                default 'constant'
        The dependence between the proportion of positive center
        inputs and acceptable proportion of positive surround
        inputs for cell with on-center (for cell with off-center
        conversely)

        - 'constant'

        - 'linear', grows linearly

        - 'elliptical', grows like a quoter of an ellipse with
            center in (1, 0) and half-axis 1-center_threshold
            and surround_threshold (see below)

    center_threshold : float, [0; 1], default 1.0
        Minimal proportion of positive (or negative for off-center
        cell's type) center inputs, required to be able to response
        positively

    surround_threshold : float, [0; 1], default 0.7
        Maximal proportion of positive (or negative for off-center
        cell's type) surround inputs, required to be able to response
        positively

    n_iter : int, optional, default 0
        The number of iterations the layer has ran


    Attributes
    ----------

    shape : tuple, (row, column)
        The shape of the layer

    n_iter : int
        The number of iterations the layer has ran

    on_cells : list
        2 dimensional array of on-center cells

    off_cells : list
        2 dimensional array of off-center cells

    input_ : numpy.ndarray
        Layer's input at the last iteration

    response : list of two numpy.ndarray
        Current response of on- and off-center cells of the layer.
        On-center cells first.

    Notes
    -----

    Yet have been developed only evenly disturbed ganglions with the same size
    of receptive fields


    """

    def __init__(self,
                 previous_layer,
                 receptive_field_shape,
                 center_surround_tolerance='linear',
                 center_threshold=0.8,
                 surround_threshold=0.2,
                 n_iter=0):
        self._previous_layer = previous_layer
        self._receptive_field_shape = receptive_field_shape
        self._center_radius, self._surround_radius = receptive_field_shape
        self.n_iter = n_iter

        self.input_ = None
        self.shape = tuple(
            np.array(self._previous_layer.shape) -
            np.full(2, 2 * self._surround_radius)
        )
        self.response = [np.empty(self.shape, dtype=np.int8) for _ in range(2)]
        self.on_cells = []
        self.off_cells = []
        self._create_cells(center_surround_tolerance,
                           center_threshold,
                           surround_threshold)

    def _create_cells(self,
                      center_surround_tolerance,
                      center_threshold,
                      surround_threshold):

        for i in range(self.shape[0]):
            self.on_cells.append([])
            self.off_cells.append([])

            for j in range(self.shape[1]):
                center_position = tuple(
                    np.array((i, j)) +
                    np.full(2, self._surround_radius)
                )

                center_input_positions, surround_input_positions = \
                    get_csarf(self._receptive_field_shape,
                              center_position
                              )

                input_cells = self._previous_layer.cells

                center_input = [input_cells[row][column]
                                for row, column in center_input_positions]
                surround_input = [input_cells[row][column]
                                  for row, column in surround_input_positions]

                self.on_cells[i].append(
                    GanglionBinaryCell(
                        position=(i, j),
                        center_type=1,
                        center_input=center_input,
                        surround_input=surround_input,
                        center_surround_tolerance=center_surround_tolerance,
                        center_threshold=center_threshold,
                        surround_threshold=surround_threshold,
                        n_iter=self.n_iter
                    )
                )
                self.off_cells[i].append(
                    GanglionBinaryCell(
                        position=(i, j),
                        center_type=-1,
                        center_input=center_input,
                        surround_input=surround_input,
                        center_surround_tolerance=center_surround_tolerance,
                        center_threshold=center_threshold,
                        surround_threshold=surround_threshold,
                        n_iter=self.n_iter
                    )
                )

    def run(self):
        """ Perform one iteration

        """
        self.input_ = self._previous_layer.response

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.on_cells[i][j].run()
                self.response[0][i][j] = self.on_cells[i][j].response
                self.off_cells[i][j].run()
                self.response[1][i][j] = self.off_cells[i][j].response

        self.n_iter += 1
