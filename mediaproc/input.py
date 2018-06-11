""" Classes for obtaining and preprocessing images and video frames.

"""
from copy import deepcopy

import cv2
import numpy as np


class ImagesGet:
    """ Class for getting visual data from a list of images

        Parameters
        ----------
        images : array-like object or np.array
            Contains a list of np.ndarray images or one image

        Attributes
        ----------

        n_iter: int
            The number of iterations the layer has ran

        Notes
        -----

        In this implementation when the end of the list is reached
        get_frame() method will continue returning the last image
        of the list.

    """

    def __init__(self, images):
        self._images = images
        self.n_iter = 0

    def _binarize_frame(self):
        # TODO: smarter binarization
        ret, self._frame = cv2.threshold(self._frame, thresh=127, maxval=1, type=cv2.THRESH_BINARY)

    def _load_new_frame(self):
        self.n_iter += 1
        if isinstance(self._images, np.ndarray):
            self._frame = self._images
        else:
            if self.n_iter >= len(self._images):
                self._frame = self._images[len(self._images)-1]
            else:
                self._frame = self._images[self.n_iter-1]
        self._binarize_frame()

    def get_frame(self):
        """ Get new frame

        """

        self._load_new_frame()
        frame = self._frame
        return frame

    def get_last_frame(self):
        """ Get the last frame

        """
        last_frame = self._frame
        return last_frame


class MechanicalEye:
    """ Class for mechanical eye simulation

        Gets an image and provides square field of view, that can
        be moved around this image using move() method.

        Parameters
        ----------
        image : np.ndarray, grayscale image
            Grayscale image with values [0, 255]

        field_size: int
            The side of square field of view

        Attributes
        ----------
        frame : np.ndarray, grayscale image
            A part of an original image corresponding to
            current position of field of view

        image : np.ndarray
            Binarized original image with pixel's values {0, 1}

        image_n_frame : np.ndarray, RGB image
            Original image with imposed field of view

        field_size : int
            The side of square field of view

        boundaries : list of 2 np.ndarray
            Upper left and lower right boundary positions of center
            of the field of view (both inclusively)

        bound_reached : bool
            True if try to move field of view outside the image

        center_position : np.ndarray, [vertical, horizontal]
            The current position of center of clear vision

        Methods
        -------
        get_frame()
        move()

        Notes
        -----
        Everywhere first coordinate [0] is vertical,
        second coordinate [1] is horizontal (as in numpy)

        self.image has the same shape as input image
        self.color_image and self.image_n_frame has additional black boundaries with thickness 1

    """

    def __init__(self, image, field_size):
        self.field_size = field_size

        # copy and binarize image (max 255)
        self.image = deepcopy(image).astype(dtype=np.uint8)
        self.image = self._binarize_img(self.image, maxval=255)

        # add white fields to the edges of color_image
        self.color_image = np.concatenate((np.zeros((1, self.image.shape[0])),
                                           self.image,
                                           np.zeros((1, self.image.shape[0]))
                                           ),
                                          axis=0
                                          )
        self.color_image = np.concatenate((np.zeros((self.image.shape[1] + 2, 1)),
                                           self.color_image,
                                           np.zeros((self.image.shape[1] + 2, 1))
                                           ),
                                          axis=1
                                          )
        self.color_image = self.color_image.astype(dtype=np.uint8)

        # colorize color_image
        self.color_image = cv2.cvtColor(self.color_image, cv2.COLOR_GRAY2RGB)

        # binarize image (max 1)
        self.image = self._binarize_img(self.image, maxval=1)

        # boundaries for center position (both inclusively)
        self.boundaries = [(field_size//2, self.image.shape[0]-1-field_size//2),
                           (field_size//2, self.image.shape[1]-1-field_size//2)]
        self.bound_reached = False

        # move field of view to initial position
        self.center_position = None
        self.point1 = None
        self.point2 = None
        self.move_initial()

    def get_frame(self):
        """ Get frame

            In this class new frame comes while method move() is called

        """

        return self.frame

    def move_initial(self):
        """ Moves field of view to the initial position
            and updates frame and visualisation

        """

        self.bound_reached = False

        self.center_position = np.array((self.field_size // 2, self.field_size // 2))
        self.point1 = np.array((0, 0))
        self.point2 = np.array((self.field_size-1, self.field_size-1))

        self._update_frame()
        self._update_visualisation()

    def move(self, displacement):
        """ Moves field of view according to displacement vector
            and updates frame and visualisation

            Parameters
            ----------
            displacement : array-like
                Displacement vector

        """
        if isinstance(displacement, (tuple, list)):
            displacement = np.array(displacement)

        new_center = self.center_position + displacement

        # check if trying to move field of view outside the image
        self.bound_reached = False

        if new_center[0] < self.boundaries[0][0]:
            new_center[0] = self.boundaries[0][0]
            self.bound_reached = True

        elif new_center[0] > self.boundaries[0][1]:
            new_center[0] = self.boundaries[0][1]
            self.bound_reached = True

        if new_center[1] < self.boundaries[1][0]:
            new_center[1] = self.boundaries[1][0]
            self.bound_reached = True
        elif new_center[1] > self.boundaries[1][1]:
            new_center[1] = self.boundaries[1][1]
            self.bound_reached = True

        if self.bound_reached:
            displacement = new_center - self.center_position

        self.center_position = new_center
        self.point1 += displacement
        self.point2 += displacement

        self._update_frame()
        self._update_visualisation()

    def _update_frame(self):
        self.frame = self.image[self.point1[0]:self.point2[0] + 1,
                                self.point1[1]:self.point2[1] + 1
                                ]

    def _update_visualisation(self):
        if self.bound_reached:
            color = (255, 0, 0)
        else:
            color = (0, 255, 0)

        self.image_n_frame = deepcopy(self.color_image)
        cv2.rectangle(self.image_n_frame,
                      pt1=tuple(self.point1[::-1]),
                      pt2=tuple(self.point2[::-1] + np.array([2, 2])),
                      color=color,
                      thickness=1
                      )

    @staticmethod
    def _binarize_img(img, maxval):
        ret, bin_img = cv2.threshold(img, thresh=127, maxval=maxval, type=cv2.THRESH_BINARY)
        return bin_img
