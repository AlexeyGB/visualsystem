""" Useful utils for structures

"""

import math

import numpy as np
import cv2
import itertools


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

        surround_input_positions : list of tuples of surrounding input
            cells positions


    """

    center_radius, surround_radius = receptive_field_shape
    center_input_positions = []
    surround_input_positions = []

    fig_center = (surround_radius, surround_radius)
    fig_size = 2*surround_radius+1
    fig_csarf = np.zeros((fig_size, fig_size))
    cv2.circle(fig_csarf, fig_center, surround_radius, -1, -1)
    cv2.circle(fig_csarf, fig_center, center_radius, 1, -1)

    center_position = np.array(center_position)

    for i in range(fig_size):
        for j in range(fig_size):
            if fig_csarf[i][j] == 1:
                # center
                center_input_positions.append(tuple(
                    np.array((i, j)) - np.array(fig_center) +
                    center_position
                ))
            elif fig_csarf[i][j] == -1:
                # surround
                surround_input_positions.append(tuple(
                    np.array((i, j)) - np.array(fig_center) +
                    center_position
                ))

    return center_input_positions, surround_input_positions


def get_simple_pvc_receptive_field(receptive_field_size, center_position, type_):
    """ Returns receptive field for Simple PVC Cell


    """

    size = receptive_field_size
    on_region_input_positions = []
    off_region_input_positions = []

    center = size//2+1
    field_center = np.full(2, center)
    cell_position = np.array(center_position)

    k1 = math.tan(math.radians(27))
    k2 = math.tan(math.radians(62))

    if type_ == 'vertical':
        for i in range(size):
            for j in range(size):
                if j == center:
                    on_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )
                elif ((center - i) / (j - center) >= k2) or ((center - i) / (j - center) <= -k2):
                    on_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )
                else:
                    off_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )

    elif type_ == 'horizontal':
        for i in range(size):
            for j in range(size):
                if j == center:
                    if i == center:
                        on_region_input_positions.append(
                            np.array((i, j)) - field_center +
                            cell_position
                        )
                elif ((center - i) / (j - center) >= -k1) and ((center - i) / (j - center) <= k1):
                    on_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )
                else:
                    off_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )

    elif type_ == 'left_inclined':
        for i in range(size):
            for j in range(size):
                if j == center:
                    if i == center:
                        on_region_input_positions.append(
                            np.array((i, j)) - field_center +
                            cell_position
                        )
                elif ((center - i) / (j - center) >= -k2) and ((center - i) / (j - center) <= -k1):
                    on_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )
                else:
                    off_region_input_positions.append(
                            np.array((i, j)) - field_center +
                            cell_position
                        )

    elif type_ == 'right_inclined':
        for i in range(size):
            for j in range(size):
                if j == center:
                    if i == center:
                        on_region_input_positions.append(
                            np.array((i, j)) - field_center +
                            cell_position
                        )
                elif ((center - i) / (j - center) >= k1) and ((center - i) / (j - center) <= k2):
                    on_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )
                else:
                    off_region_input_positions.append(
                        np.array((i, j)) - field_center +
                        cell_position
                    )

    return on_region_input_positions, off_region_input_positions
