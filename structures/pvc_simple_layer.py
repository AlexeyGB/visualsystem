""" The models of a layer of simple cells of Primary Visual Cortex (PVC)

"""


from copy import deepcopy
import itertools


import numpy as np


from ._base import get_simple_pvc_receptive_field
from ..cells.pvc import SimplePVCBinaryCell


SIMPLE_PVC_TYPES = ['vertical', 'horizontal', 'left_inclined', 'right_inclined']


class SimplePVCBinaryLayer:
    """ Class for layer of binary Simple PVC cells
        Provides 4 sublayer, which detects vertical, horizontal,
        inclined to the left and inclined to the right borders

        Parameters
        ----------

        previous_layer : object
            An object of bipolar's layer

        receptive_field_size : int, must be odd

        input_sublayer_type : {'on-center', 'off-center', 'both'}
            There is three alternatives:

            - 'on-center', only cells from sublayer with on-center cells are
                at the input

            - 'off-center', only cells from sublayer with off-center cells are
                at the input

            - 'both', cells from both sublayers are at the input

        regions_tolerance :  {'constant', 'linear', 'elliptical'},
                             default 'constant'
            The dependence between the proportion of positive on-region's
            inputs and acceptable proportion of positive off-region's
            inputs

            - 'constant'

            - 'linear', grows linearly

            - 'elliptical', grows like a quoter of an ellipse with
                center in (1, 0) and half-axis 1-on_region_threshold
                and off_region_threshold (see below)

        on_region_threshold : float, [0; 1], default 1.0
            Minimal proportion of positive on-region's inputs, required to be able
            to response positively

        off_region_threshold : float, [0; 1], default 0.0
            Maximal proportion of positive off-region's inputs, required to be able
            to response positively

        n_iter : int, optional, default 0
            The number of iterations the layer has ran

        Attributes
        ----------
        shape : tuple, (row, column)
            The shape of the layer

        n_iter : int
            The number of iterations the layer has ran

        cells : dict
            The dict of layer's cells divided by sublayers:
            ['vertical', 'horizontal', 'left_inclined', 'right_inclined']

        input_ : list of two numpy.ndarray
            Layer's input at the last iteration.

        response : dict
            Current response of cells of the layer. Divided by sublayers:
            ['vertical', 'horizontal', 'left_inclined', 'right_inclined']

        Notes
        -----


    """

    def __init__(self,
                 previous_layer,
                 receptive_field_size,
                 input_sublayer_type,
                 regions_tolerance='constant',
                 on_region_threshold=1.0,
                 off_region_threshold=0.0,
                 n_iter=0
                 ):
        self._previous_layer = previous_layer
        self._receptive_field_size = receptive_field_size
        self._input_sublayer_type = input_sublayer_type
        self.n_iter = n_iter

        self.input_ = None
        self.shape = tuple(
            np.array(self._previous_layer.shape) -
            np.full(2, self._receptive_field_size - 1)
        )
        self.response = {type_: np.empty(self.shape, dtype=np.int8)
                         for type_ in SIMPLE_PVC_TYPES}

        self.cells = {type_: [] for type_ in SIMPLE_PVC_TYPES}
        self._create_cells(regions_tolerance,
                           on_region_threshold,
                           off_region_threshold
                           )

    def _create_cells(self,
                      regions_tolerance,
                      on_region_threshold,
                      off_region_threshold
                      ):
        for type_ in self.cells.keys():

            for i in range(self.shape[0]):
                self.cells[type_].append([])

                for j in range(self.shape[1]):
                    center_position = tuple(
                        np.array((i, j)) +
                        np.full(2, self._receptive_field_size//2)
                    )

                    on_region_input_positions, off_region_input_positions = \
                        get_simple_pvc_receptive_field(self._receptive_field_size,
                                                       center_position,
                                                       type_
                                                       )

                    if self._input_sublayer_type == 'on-center':
                        on_region_input = [self._previous_layer.on_cells[i][j]
                                           for i, j in on_region_input_positions]
                        off_region_input = [self._previous_layer.on_cells[i][j]
                                            for i, j in off_region_input_positions]

                    elif self._input_sublayer_type == 'off-center':
                        on_region_input = [self._previous_layer.off_cells[i][j]
                                           for i, j in on_region_input_positions]
                        off_region_input = [self._previous_layer.off_cells[i][j]
                                            for i, j in off_region_input_positions]

                    elif self._input_sublayer_type == 'both':
                        on_region_input = []
                        off_region_input = []

                        # on-cells
                        on_region_input.append(
                            [self._previous_layer.on_cells[i][j]
                            for i, j in on_region_input_positions]
                        )
                        off_region_input.append(
                            [self._previous_layer.on_cells[i][j]
                            for i, j in off_region_input_positions]
                        )
                        # off-cells
                        on_region_input.append(
                            [self._previous_layer.off_cells[i][j]
                             for i, j in on_region_input_positions]
                        )
                        off_region_input.append(
                            [self._previous_layer.off_cells[i][j]
                             for i, j in off_region_input_positions]
                        )

                    self.cells[type_][i].append(
                        SimplePVCBinaryCell(
                            position=(i, j),
                            input_sublayer_type=self._input_sublayer_type,
                            on_region_input=on_region_input,
                            off_region_input=off_region_input,
                            regions_tolerance=regions_tolerance,
                            on_region_threshold=on_region_threshold,
                            off_region_threshold=off_region_threshold,
                            n_iter=self.n_iter
                        )
                    )

    def run(self):
        """ Perform one iteration

        """

        self.input_ = deepcopy(self._previous_layer.response)

        for type_ in self.cells.keys():
            for i, j in itertools.product(range(self.shape[0]),
                                          range(self.shape[1])):
                self.cells[type_][i][j].run()
                self.response[type_][i][j] = self.cells[type_][i][j].response

        self.n_iter += 1