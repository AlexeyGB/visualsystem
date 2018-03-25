""" Classes for obtaining and preprocessing images and video frames.

"""


class ImagesGet:
    """ Class for getting visual data from a list of images

        Parameters
        ----------
        images : array-like object
            Contains a list of images.

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

    def _load_new_frame(self):
        self.n_iter += 1
        if self.n_iter >= len(self._images):
            self._frame = self._images[len(self._images)-1]
        else:
            self._frame = self._images[self.n_iter-1]


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

class VideoFrameGet:
    pass
