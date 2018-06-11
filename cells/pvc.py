""" Models of cells of Primary Visual Cortex (V1) (here - PVC)

"""


import numpy as np


from ._base import tolerance_line, tolerance_ellipse


class SimplePVCBinaryCell:
    """ Binary simple primary virtual cortex's cell class

    Parameters
    ----------

    position : tuple, (row, column)
            The position of the cell in its layer

    input_sublayer_type : {'on-center', 'off-center', 'both'}
        There is three alternatives:

        - 'on-center', only cells from sublayer with on-center cells are
            at the input

        - 'off-center', only cells from sublayer with off-center cells are
            at the input

        - 'both', cells from both sublayers are at the input

    on_region_input : array-like or list of two arrays,
                      depending on input_sublayer_type.
        Array (or two) of references to cells related to the on-region of
        the receptive field. If two, the first must be sublayer with
        on-center cells.

    off_region_input : array-like or array of two arrays, depending on
                       input_sublayer_type.
        Array (or two) of references to cells related to the off-region of
        the receptive field. If two, the first must be sublayer with
        on-center cells.

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
        The number of iterations the cell has ran

    Attributes
    ----------

    position : tuple, (row, column)
        The position of the cell in its layer

    n_iter : int
        The number of iterations the cell has ran

    input_sublayer_type : {'on-center', 'off-center', 'both'}
        There is three alternatives:

        - 'on-center', only cells from sublayer with on-center cells are
            at the input

        - 'off-center', only cells from sublayer with off-center cells are
            at the input

        - 'both', cells from both sublayers are at the input

    response : int, {0, 1}
        Current cell's response

    Notes
    -----
    The functionality is moved to SimplePVCBinary2
    Stays here just for keeping some old code working.

    """

    def __init__(self, position,
                 input_sublayer_type,
                 on_region_input,
                 off_region_input,
                 regions_tolerance='constant',
                 on_region_threshold=1.0,
                 off_region_threshold=0.0,
                 n_iter=0
                 ):
        self.position = position
        self.n_iter = n_iter
        self.input_sublayer_type = input_sublayer_type
        self._on_region_input = on_region_input
        self._off_region_input = off_region_input
        self._regions_tolerance = regions_tolerance
        self._on_region_threshold = on_region_threshold
        self._off_region_threshold = off_region_threshold
        self.response = 0
        
    def _calculate_response(self, on_region_inputs, off_region_inputs):

        on_region_positive_in_share = np.mean(on_region_inputs)
        off_region_positive_in_share = np.mean(off_region_inputs)

        if self._regions_tolerance == 'constant':
            if (on_region_positive_in_share >= self._on_region_threshold) and \
               (off_region_positive_in_share <= self._off_region_threshold):

                response = 1
            else:
                response = 0

        elif self._regions_tolerance == 'linear':
            if off_region_positive_in_share <= \
                    tolerance_line(on_region_positive_in_share,
                                   self._on_region_threshold,
                                   self._off_region_threshold
                                   ):
                response = 1
            else:
                response = 0

        elif self._regions_tolerance == 'elliptical':
            if off_region_positive_in_share <= \
                    tolerance_ellipse(on_region_positive_in_share,
                                      self._on_region_threshold,
                                      self._off_region_threshold
                                      ):
                response = 1
            else:
                response = 0

        return response

    def run(self):
        """ Perform one iteration

        """

        if (self.input_sublayer_type == 'on-center') or \
           (self.input_sublayer_type == 'off-center'):
            on_region_inputs = \
                [cell.response for cell in self._on_region_input]
            off_region_inputs = \
                [cell.response for cell in self._off_region_input]

            self.response = self._calculate_response(
                on_region_inputs,
                off_region_inputs
            )

        elif self.input_sublayer_type == 'both':

            on_region_inputs_1 = \
                [cell.response for cell in self._on_region_input[0]]
            off_region_inputs_1 = \
                [cell.response for cell in self._off_region_input[0]]

            on_region_inputs_2 = \
                [cell.response for cell in self._on_region_input[1]]
            off_region_inputs_2 = \
                [cell.response for cell in self._off_region_input[1]]

            response_1 = self._calculate_response(
                on_region_inputs_1,
                off_region_inputs_1
            )
            response_2 = self._calculate_response(
                on_region_inputs_2,
                off_region_inputs_2
            )

            self.response = response_1 * response_2

        self.n_iter += 1


class SimplePVCBinaryCell2:
    """ Binary simple primary virtual cortex's cell class

    Parameters
    ----------

    position : tuple, (row, column)
            The position of the cell in its layer

    on_region_input : array-like or list of two arrays,
                      depending on input_sublayer_type.
        Array (or two) of references to cells related to the on-region of
        the receptive field. If two, the first must be sublayer with
        on-center cells.

    off_region_input : array-like or array of two arrays, depending on
                       input_sublayer_type.
        Array (or two) of references to cells related to the off-region of
        the receptive field. If two, the first must be sublayer with
        on-center cells.

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
        The number of iterations the cell has ran

    Attributes
    ----------

    position : tuple, (row, column)
        The position of the cell in its layer

    n_iter : int
        The number of iterations the cell has ran

    response : int, {0, 1}
        Current cell's response

    Notes
    -----

    """

    def __init__(self, position,
                 on_region_input,
                 off_region_input,
                 regions_tolerance='constant',
                 on_region_threshold=1.0,
                 off_region_threshold=0.0,
                 n_iter=0
                 ):
        self.position = position
        self.n_iter = n_iter
        self._on_region_input = on_region_input
        self._off_region_input = off_region_input
        self._regions_tolerance = regions_tolerance
        self._on_region_threshold = on_region_threshold
        self._off_region_threshold = off_region_threshold
        self.response = 0

    def _calculate_response(self, on_region_inputs, off_region_inputs):

        on_region_positive_in_share = np.mean(on_region_inputs)
        off_region_positive_in_share = np.mean(off_region_inputs)

        if self._regions_tolerance == 'constant':
            if (on_region_positive_in_share >= self._on_region_threshold) and \
                    (off_region_positive_in_share <= self._off_region_threshold):

                response = 1
            else:
                response = 0

        elif self._regions_tolerance == 'linear':
            if off_region_positive_in_share <= \
                    tolerance_line(on_region_positive_in_share,
                                   self._on_region_threshold,
                                   self._off_region_threshold
                                   ):
                response = 1
            else:
                response = 0

        elif self._regions_tolerance == 'elliptical':
            if off_region_positive_in_share <= \
                    tolerance_ellipse(on_region_positive_in_share,
                                      self._on_region_threshold,
                                      self._off_region_threshold
                                      ):
                response = 1
            else:
                response = 0

        return response

    def run(self):
        """ Perform one iteration

        """

        on_region_inputs = \
            [cell.response for cell in self._on_region_input]
        off_region_inputs = \
            [cell.response for cell in self._off_region_input]

        self.response = self._calculate_response(
            on_region_inputs,
            off_region_inputs
        )

        self.n_iter += 1