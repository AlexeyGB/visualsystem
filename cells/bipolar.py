""" Bipolar cell models

"""

from ._base import BaseCell


class BipolarBinary(BaseCell):
    """ Binary bipolar cell class

        Parameters
        ----------
        position : tuple, (row, column)
            The position of the cell in its layer

        input_ : numpy array
            Outputs of the previous level's cells

        receptive_field_сenter : array of references to cells related
            to the center of the receptive field

        receptive_field_periphery : array of references to cells related
            to the periphery of the receptive field

        center_periphery_ratio : float, default 1.0
            The ratio used in response calculations (see Notes)

        center_type : int, {0, 1}, default 1
            The type of cell's receptive field

            - 0, receptive field with off-center

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

            - 0, receptive field with off-center

            - 1, receptive field with on-center

        Notes
        -----
        For cells with receptive field with on-center response is calculated as follows:

        Response = 1, if (center_periphery_ratio * sum(center)/n_center -
                          sum(periphery)/n_periphery) > 0
                   0, else

        For cells with receptive field with on-center response is calculated conversely.


    """

    def __init__(self, position, input_, receptive_field_сenter,
                 receptive_field_periphery, center_periphery_ratio=1.0,
                 center_type=1, n_iter=0):
        super().__init__(position, input_, n_iter)
        self._receptive_field_center = receptive_field_сenter
        self._receptive_field_periphery = receptive_field_periphery
        self._center_periphery_ratio = center_periphery_ratio
        self.center_type = center_type
        self._response = 0

    def _calculate_response(self):
        central_in = 0
        for central_cell in self._receptive_field_center:
            central_in += central_cell.get_response()

        peripheral_in = 0
        for peripheral_cell in self._receptive_field_periphery:
            peripheral_in += peripheral_cell.get_response()

        total_in = (self._center_periphery_ratio *
                    central_in / len(self._receptive_field_center) -
                    peripheral_in / len(self._receptive_field_periphery))

        if self.center_type:
            if total_in > 0:
                response = 1
            else:
                response = 0
        else:
            if total_in < 0:
                response = 1
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
