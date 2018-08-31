"""
Models of human's visual system

"""

from copy import deepcopy

from ..mediaproc.input import ImagesGet
from .photoreceptors_layer import RodsBinaryLayer
from .ganglions_layer import GanglionsBinaryLayer
from .pvc_simple_layer import SimplePVCBinaryLayer


class EyeModelAlpha:
    """
    Network's scheme:
    ImagesGet -> RodsBinaryLayer -> GanglionsBinaryLayer ->
    -> SimplePVCBinaryLayer -> output

    Parameters
    ----------

    data_get_params : dict
        Parameters for data_get class.
        Is used like **kwargs

    receptors_params : dict
        Parameters for receptors layer class.
        Is used like **kwargs

    ganglions_params : dict
        Parameters for bipolars layer class.
        Is used like **kwargs

    pvc_params : dict
        Parameters for PVCs layer class.
        Is used like **kwargs

    data_get : class, default ImagesGet
        Class must provides get_frame method that
        returns current system's input image

    receptors : class, default RodsBinaryLayer
        Class of receptor

    ganglions : class, default GanglionsBinaryLayer
        Class of ganglion cells. Recognises edges.

    pvc : class, default SimplePVCBinaryLayer
        Class of PVC cells. Recognises directed lines.

    n_iter : int, default 0
        The number of iterations the layer has ran

    Attributes
    ----------

    n_iter : int
        The number of iterations the layer has ran
    """

    def __init__(self,
                 data_get_params,
                 receptors_params,
                 ganglions_params,
                 pvc_params,
                 data_get=ImagesGet,
                 receptors=RodsBinaryLayer,
                 ganglions=GanglionsBinaryLayer,
                 pvc=SimplePVCBinaryLayer,
                 n_iter=0
                 ):
        self.data_get_layer = data_get(**data_get_params)
        self.receptors_layer = receptors(data_source=self.data_get_layer, **receptors_params)
        self.ganglions_layer = ganglions(self.receptors_layer, **ganglions_params)
        self.pvc_layer = pvc(self.ganglions_layer, **pvc_params)
        self.n_iter = n_iter

    def run(self):
        self.receptors_layer.run()
        self.ganglions_layer.run()
        self.pvc_layer.run()

        self.n_iter += 1

    def get_input(self):
        return deepcopy(self.data_get_layer.get_last_frame())

    def get_ganglion_response(self):
        return deepcopy(self.ganglions_layer.response)

    def get_pvc_response(self):
        return deepcopy(self.pvc_layer.response)
