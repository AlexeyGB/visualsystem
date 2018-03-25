""" Useful things for cells

"""


def tolerance_line(x, x1, y2):
    """ Linear tolerance function

        Parameters
        ----------
        x : float, [0, 1]
            Current proportion of positive (or negative for off-center
            cell's type) central inputs

        x1 : float, [0, 1]
            Minimal proportion of positive (or negative for off-center
            cell's type) central inputs, required to be able to response
            positively

        y2 : float, [0, 1]
            Maximal proportion of positive (or negative for off-center
            cell's type) peripheral inputs, required to be able to response
            positively

        Returns
        -------
        Maximal proportion of positive (or negative for off-center
        cell's type) peripheral inputs, where the response is positive

    """

    if x > x1:
        return y2 / (1 - x1) * x + y2 / (x1 - 1) * x1
    else:
        return -1


def tolerance_ellipse(x, x1, y2):
    """ Elliptical tolerance function

        Parameters
        ----------
        x : float, [0, 1]
            Current proportion of positive (or negative for off-center
            cell's type) central inputs

        x1 : float, [0, 1]
            Minimal proportion of positive (or negative for off-center
            cell's type) central inputs, required to be able to response
            positively

        y2 : float, [0, 1]
            Maximal proportion of positive (or negative for off-center
            cell's type) peripheral inputs, required to be able to response
            positively

        Returns
        -------
        Maximal proportion of positive (or negative for off-center
        cell's type) peripheral inputs, where the response is positive
    """

    if x > x1:
        return y2 * (1 - (x - 1) ** 2 / (x1 - 1) ** 2) ** 0.5
    else:
        return -1
