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

        input_surround : array-like
            Array of references to cells related
            to the surround of the receptive field

        center_surround_tolerance : {'linear', 'elliptical'}
            The dependence between the proportion of positive center
            inputs and acceptable proportion of positive surround
            inputs for cell with on-center (for cell with off-center
            conversely)

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
                 input_surround, center_surround_tolerance='linear',
                 center_threshold=0.8, surround_threshold=0.2,
                 center_type=1, n_iter=0):
        self.position = position
        self.n_iter = n_iter
        self._input_center = input_center
        self._input_surround = input_surround
        self._center_surround_tolerance = center_surround_tolerance
        self._center_threshold = center_threshold
        self._surround_threshold = surround_threshold
        self.center_type = center_type
        self._response = 0

    def _calculate_response(self):
        center_in = 0
        for center_cell in self._input_center:
            center_in += center_cell.get_response()

        surround_in = 0
        for surround_cell in self._input_surround:
            surround_in += surround_cell.get_response()

        if self.center_type == 1:
            center_positive_in_share = center_in/len(self._input_center)
            surround_positive_in_share = surround_in/len(self._input_surround)
        else:
            center_positive_in_share = 1 - center_in/len(self._input_center)
            surround_positive_in_share = 1 - surround_in/len(self._input_surround)

        if self._center_surround_tolerance == 'linear':
            if surround_positive_in_share <= tolerance_line(center_positive_in_share,
                                                              self._center_threshold,
                                                              self._surround_threshold
                                                              ):
                response = 1
            else:
                response = 0

        elif self._center_surround_tolerance == 'elliptical':
            if surround_positive_in_share <= tolerance_ellipse(center_positive_in_share,
                                                                 self._center_threshold,
                                                                 self._surround_threshold
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
