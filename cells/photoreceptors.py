""" Photoreceptor cells models

"""


class RodBinaryCell:
    """ Binary rod cell class

        Parameters
        ----------
        position : tuple, (row, column)
            The position of the cell in its layer

        n_iter : int, optional, default 0
            The number of iterations the cell has ran

        Attributes
        ----------
        position: tuple, (row, column)
            The position of the cell in its layer

        n_iter : int
            The number of iterations the cell has ran

        Notes
        -----

        So far only the case when input image is binary is implemented.
        todo: make a binorization method


    """

    def __init__(self, position, n_iter=0):
        self.position = position
        self.n_iter = n_iter
        self.response = 0

    def run(self, input_):
        """ Perform one iteration

            Parameters
            ----------
            input_ : numpy array
                Whole image in black and white (valid values of each
                pixel: {0, 1})
        """

        self.response = input_[self.position]
        self.n_iter += 1
