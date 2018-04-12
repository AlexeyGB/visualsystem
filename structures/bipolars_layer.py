""" The models of layer of bipolar cells

"""


from copy import deepcopy

import numpy as np

from ..cells.bipolar import BipolarBinaryCell
from ._base import get_csarf


class BipolarsBinaryLayer:
    """ Class for layer of binary bipolar cells
        Provides two sublayers: of on-center and off-center cells.

    Parameters
    ----------

    previous_layer: object
        An object of a rod's layer

    receptive_field_shape : tuple, {center_radius, surround_radius}

    center_surround_tolerance : {'constant', 'linear', 'elliptical'},
                                default 'linear'
        The dependence between the proportion of positive center
        inputs and acceptable proportion of positive surround
        inputs for cell with on-center (for cell with off-center
        conversely)

        - 'constant'

        - 'linear', grows linearly

        - 'elliptical', grows like a quoter of an ellipse with
            center in (1, 0) and half-axis 1-center_threshold
            and surround_threshold (see below)

    center_threshold : float, [0; 1], default 0.8
        Minimal proportion of positive (or negative for off-center
        cell's type) center inputs, required to be able to response
        positively

    surround_threshold : float, [0; 1], default 0.2
        Maximal proportion of positive (or negative for off-center
        cell's type) surround inputs, required to be able to response
        positively

    n_iter : int, optional, default 0
        The number of iterations the layer has ran


    Attributes
    ----------

    shape: tuple, (row, column)
        The shape of the layer

    n_iter: int
        The number of iterations the layer has ran

    on_cells : list
        2 dimensional array of on-center cells

    off_cells : list
        2 dimensional array of off-center cells

    input_: numpy array
        Layer's input at the last iteration
        Array's shape is equal to layer's shape

    on_response: numpy array
        On-center cells of the layer's current response
        Array's shape is equal to layer's shape

    off_response:
        Off-center cells of the layer's current response
        Array's shape is equal to layer's shape

    Notes
    -----

    Yet have been developed only evenly disturbed bipolars with the same size
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
            2 * np.array(
                (self._surround_radius, self._surround_radius)
            )
        )
        self.on_response = np.empty(self.shape, dtype=np.int8)
        self.off_response = np.empty(self.shape, dtype=np.int8)
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
                    np.array(
                        (self._surround_radius, self._surround_radius)
                    )
                )

                center_input_position, surround_input_position = \
                    get_csarf(self._receptive_field_shape,
                              center_position
                              )

                input_cells = self._previous_layer.cells

                center_input = [input_cells[row][column]
                                for row, column in center_input_position]
                surround_input = [input_cells[row][column]
                                  for row, column in surround_input_position]

                self.on_cells[i].append(
                    BipolarBinaryCell(
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
                    BipolarBinaryCell(
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
        self.input_ = deepcopy(self._previous_layer.response)

        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                self.on_cells[i][j].run()
                self.on_response[i][j] = self.on_cells[i][j].response
                self.off_cells[i][j].run()
                self.off_response[i][j] = self.off_cells[i][j].response

        self.n_iter += 1
