""" Useful utils for structures

"""

import numpy as np
import cv2


def get_csarf(receptive_field_shape, center_position):
    """ CSARF: Center-surround antagonistic receptive field

        Parameters
        ----------
        receptive_field_shape : tuple, (center_radius, surround_radius)
            center_radius : int
                Radius of central part of CSARF
            surround_radius : int
                Radius of surrounding part pf CSARF

        center_position : tuple, (row, column)
            Position of center of receptive field

        Returns
        -------
        csarf : tuple, (center_input_positions, surround_input_positions)
            center_input_positions : list of tuples of central input cells
            positions
            surround_input_positions : list of tuples of surrounding input cells
            positions


    """

    center_radius, surround_radius = receptive_field_shape
    center_input_positions = []
    surround_input_positions = []

    fig_center_coordinates = (surround_radius, surround_radius)
    fig_size = 2*surround_radius+1
    fig_csarf = np.zeros((fig_size, fig_size))
    cv2.circle(fig_csarf, fig_center_coordinates, surround_radius, -1, -1)
    cv2.circle(fig_csarf, fig_center_coordinates, center_radius, 1, -1)

    cell_position = np.array(center_position)

    for i in range(fig_size):
        for j in range(fig_size):
            if fig_csarf[i][j] == 1:
                # center
                center_input_positions.append(tuple(
                    np.array((i, j)) - np.array(fig_center_coordinates) +
                    np.array(cell_position)
                ))
            elif fig_csarf[i][j] == -1:
                # surround
                surround_input_positions.append(tuple(
                    np.array((i, j)) - np.array(fig_center_coordinates) +
                    np.array(cell_position)
                ))

    return center_input_positions, surround_input_positions
