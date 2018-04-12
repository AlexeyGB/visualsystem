""" Bipolar cell models

"""


from ._base import tolerance_line, tolerance_ellipse


class BipolarBinaryCell:
    """ Binary bipolar cell class

        Parameters
        ----------

        position : tuple, (row, column)
            The position of the cell in its layer

        center_type : int, {-1, 1}, default 1
            The type of cell's receptive field

            - -1, receptive field with off-center

            - 1, receptive field with on-center

        center_input : array-like
            Array of references to cells related
            to the center of the receptive field

        surround_input : array-like
            Array of references to cells related
            to the surround of the receptive field

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
            The number of iterations the cell has ran

        Attributes
        ----------
        position: tuple, (row, column)
            The position of the cell in its layer

        n_iter : int
            The number of iterations the cell has ran

        center_type : int, {-1, 1}
            The type of cell's receptive field

            - -1, receptive field with off-center

            - 1, receptive field with on-center
        
        response : int, {0, 1}
            Current cell's response

        Notes
        -----

    """

    def __init__(self, position,
                 center_input,
                 surround_input,
                 center_type=1,
                 center_surround_tolerance='linear',
                 center_threshold=0.8,
                 surround_threshold=0.2,
                 n_iter=0):

        self.position = position
        self.n_iter = n_iter
        self._center_input = center_input
        self._surround_input = surround_input
        self.center_type = center_type
        self._center_surround_tolerance = center_surround_tolerance
        self._center_threshold = center_threshold
        self._surround_threshold = surround_threshold
        self.response = 0

    def _calculate_response(self):
        center_in = 0
        for center_cell in self._center_input:
            center_in += center_cell.response

        surround_in = 0
        for surround_cell in self._surround_input:
            surround_in += surround_cell.response

        if self.center_type == 1:
            center_positive_in_share = center_in/len(self._center_input)
            surround_positive_in_share = surround_in/len(self._surround_input)
        else:
            center_positive_in_share = 1 - center_in/len(self._center_input)
            surround_positive_in_share = 1 - surround_in/len(self._surround_input)

        if self._center_surround_tolerance == 'constant':
            if (center_positive_in_share >= self._center_threshold) and \
               (surround_positive_in_share <= self._surround_threshold):

                response = 1
            else:
                response = 0

        elif self._center_surround_tolerance == 'linear':
            if surround_positive_in_share <= \
                    tolerance_line(center_positive_in_share,
                                   self._center_threshold,
                                   self._surround_threshold
                                   ):
                response = 1
            else:
                response = 0

        elif self._center_surround_tolerance == 'elliptical':
            if surround_positive_in_share <= \
                    tolerance_ellipse(center_positive_in_share,
                                      self._center_threshold,
                                      self._surround_threshold
                                      ):
                response = 1
            else:
                response = 0

        return response

    def run(self):
        """ Perform one iteration

        """

        self.response = self._calculate_response()
        self.n_iter += 1
