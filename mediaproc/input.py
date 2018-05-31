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

        Gets an image and provides field of view, that can be moved
        around this image using move() method.

        Parameters
        ----------
        image : np.ndarray
            Grayscale image with values [0, 255]

        field_size: int
            The side of square field of view

        Attributes
        ----------
        image_n_frame : RGB image
            Original image with imposed field of view

        field_size : int
            The side of square field of view

        bound_reached : bool
            True if try to move field of view outside the image

        Methods
        -------
        get_frame()
        move()

        Notes
        -----
        Everywhere first coordinate [0] is vertical,
        second coordinate [1] is horizontal


    """

    def __init__(self, image, field_size):
        self.field_size = field_size

        # color image
        image = image.astype(dtype=np.uint8)
        self.color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # add white fields to the edges of image
        self.image = self._binarize_img(image)
        self.image = np.concatenate((np.zeros((1, image.shape[0])),
                                     self.image,
                                     np.zeros((1, image.shape[0]))
                                     ),
                                    axis=0
                                    )
        self.image = np.concatenate((np.zeros((image.shape[1]+2, 1)),
                                     self.image,
                                     np.zeros((image.shape[1]+2, 1))
                                     ),
                                    axis=1
                                    )

        # boundaries for center position
        self.boundaries = [(1+field_size//2, self.image.shape[0]-1-field_size//2),
                           (1+field_size//2, self.image.shape[1]-1-field_size//2)]
        self.bound_reached = False

        # move field of view to initial position
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

        self.center = np.array((self.field_size // 2 + 1, self.field_size // 2 + 1))
        self.point1 = np.array((1, 1))
        self.point2 = np.array((self.field_size, self.field_size))

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

        new_center = self.center + displacement

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
            displacement = new_center - self.center

        self.center = new_center
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
                      pt1=tuple(self.point1[::-1] - np.array([1, 1])),
                      pt2=tuple(self.point2[::-1] + np.array([1, 1])),
                      color=color,
                      thickness=1
                      )

    def _binarize_img(self, img):
        ret, bin_img = cv2.threshold(img, thresh=127, maxval=1, type=cv2.THRESH_BINARY)
        return bin_img
