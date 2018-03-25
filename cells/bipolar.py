""" Bipolar cell models

"""


from ._base import tolerance_line, tolerance_ellipse


class BipolarBinary:
    """ Binary bipolar cell class

        Parameters
        ----------
        position : tuple, (row, column)
            The position of the cell in its layer

        input_center : array-like
            Array of references to cells related
            to the center of the receptive field

        input_periphery : array-like
            Array of references to cells related
            to the periphery of the receptive field

        central_peripheral_tolerance : {'linear', 'elliptical'}
            The dependence between the proportion of positive central
            inputs and acceptable proportion of positive peripheral
            inputs for cell with on-center (for cell with off-center
            conversely)

            - 'linear', grows linearly

            - 'elliptical', grows like a quoter of an ellipse with
                center in (1, 0) and half-axis 1-central_threshold
                and peripheral_threshold (see below)

        central_threshold : float, [0; 1], default 0.8
            Minimal proportion of positive (or negative for off-center
            cell's type) central inputs, required to be able to response
            positively

        peripheral_threshold : float, [0; 1], default 0.2
            Maximal proportion of positive (or negative for off-center
            cell's type) peripheral inputs, required to be able to response
            positively

        center_type : int, {-1, 1}, default 1
            The type of cell's receptive field

            - -1, receptive field with off-center

            - 1, receptive field with on-center

        n_iter : int, optional, default 0
            The number of iterations the cell has ran

        Attributes
        ----------
        position: tuple, (row, column)
            The position of the cell in its layer

        n_iter : int
            The number of iterations the cell has ran

        center_type : int, {0, 1}
            The type of cell's receptive field

            - -1, receptive field with off-center

            - 1, receptive field with on-center

        Notes
        -----

    """

    def __init__(self, position, input_center,
                 input_periphery, central_peripheral_tolerance='linear',
                 central_threshold=0.8, peripheral_threshold=0.2,
                 center_type=1, n_iter=0):
        self.position = position
        self.n_iter = n_iter
        self._input_center = input_center
        self._input_periphery = input_periphery
        self._central_peripheral_tolerance = central_peripheral_tolerance
        self._central_threshold = central_threshold
        self._peripheral_threshold = peripheral_threshold
        self.center_type = center_type
        self._response = 0

    def _calculate_response(self):
        central_in = 0
        for central_cell in self._input_center:
            central_in += central_cell.get_response()

        peripheral_in = 0
        for peripheral_cell in self._input_periphery:
            peripheral_in += peripheral_cell.get_response()

        if self.center_type == 1:
            central_positive_in_share = central_in/len(self._input_center)
            peripheral_positive_in_share = peripheral_in/len(self._input_periphery)
        else:
            central_positive_in_share = 1 - central_in/len(self._input_center)
            peripheral_positive_in_share = 1 - peripheral_in/len(self._input_periphery)

        if self._central_peripheral_tolerance == 'linear':
            if peripheral_positive_in_share <= tolerance_line(central_positive_in_share,
                                                              self._central_threshold,
                                                              self._peripheral_threshold
                                                              ):
                response = 1
            else:
                response = 0

        elif self._central_peripheral_tolerance == 'elliptical':
            if peripheral_positive_in_share <= tolerance_ellipse(central_positive_in_share,
                                                                 self._central_threshold,
                                                                 self._peripheral_threshold
                                                                 ):
                response = 1
            else:
                response = 0
        else:
            response = 0

        return response

    def run(self):
        """ Perform one iteration

        """

        self._response = self._calculate_response()
        self.n_iter += 1

    def get_response(self):
        """ Getting cell's current response

            Returns
            -------
            response: int, {0, 1}

        """

        response = self._response
        return response
