""" Photoreceptor cells models

"""

from ._base import BaseCell


class RodBinary(BaseCell):
    """ Binary rod cell class

        Parameters
        ----------
        position : tuple, (row, column)
            The position of the cell in its layer

        input_ : numpy array
            Whole image in black and white (valid values of each
            pixel: {0, 1})

        n_iter : int, optional, default 0
            The number of iterations the cell has ran

        Attributes
        ----------
        position: tuple, (row, column)
            The position of the cell in its layer

        n_iter : int
            The number of iterations the cell has ran


    """

    def __init__(self, position, input_, n_iter=0):
        super().__init__(position, input_, n_iter)
        self._response = 0

    def run(self):
        """ Perform one iteration

        """

        self._response = self._input[self.position]
        self.n_iter += 1

    def get_response(self):
        """ Getting cell's current response

            Returns
            -------
            response: int, {0, 1}
        """

        response = self._response
        return response
