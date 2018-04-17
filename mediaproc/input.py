""" Classes for obtaining and preprocessing images and video frames.

"""

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
