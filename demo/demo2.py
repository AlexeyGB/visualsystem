"""

"""

import cv2
import numpy as np
import sys

sys.path.append('/Users/alexey_bauman/projects/bionic_eye/')

from visualsystem.mediaproc.input import MechanicalEye
from visualsystem.structures.photoreceptors_layer import RodsBinaryLayer2
from visualsystem.structures.ganglions_layer import GanglionsBinaryLayer2
from visualsystem.structures.pvc_simple_layer import SimplePVCBinaryLayer2, SIMPLE_PVC_TYPES

# windows' positions
MECH_EYE_WIN_X          =0
MECH_EYE_WIN_Y          =30
FRAME_WIN_X             =230
FRAME_WIN_Y             =30
GANGL_WIN_X             =440
GANGL_WIN_Y             =30
PVC_VERTICAL_WIN_X      =230
PVC_VERTICAL_WIN_Y      =280
PVC_HORIZONTAL_WIN_X    =432
PVC_HORIZONTAL_WIN_Y    =280
PVC_LEFT_WIN_X          =230
PVC_LEFT_WIN_Y          =505
PVC_RIGHT_WIN_X         =432
PVC_RIGHT_WIN_Y         =505
BORDERS_WIN_X           =0
BORDERS_WIN_Y           =270

# keycodes

UP_ARROW                   = 0
DOWN_ARROW                 = 1
LEFT_ARROW                 = 2
RIGHT_ARROW                = 3


class BordersMap:
    def __init__(self, eye, gangl):
        self.eye = eye
        self.gangl = gangl
        self.gangl_center = (gangl.shape[0]//2, gangl.shape[1]//2)

        self.map = np.zeros(eye.image.shape, dtype=np.uint8)

    def run(self):
        gangl_resp = self.gangl.response
        center_pos = tuple(self.eye.center_position)
        if gangl_resp[self.gangl_center] == 1:
            self.map[center_pos] = 1


class MovingDecisions:
    """

    Attributes
    ----------
    displacement : tuple, (x1, x2)
        Where x1, x2 int, x1 - vertical, x2 - horizontal

    Notes
    -----
    Documentation is not complete

    """
    def __init__(self):
        self.displacement = (0, 0)

    def run(self):
        key = cv2.waitKey(0)

        if key == LEFT_ARROW:
            self.displacement = (0, -1)
        elif key == RIGHT_ARROW:
            self.displacement = (0, 1)
        elif key == UP_ARROW:
            self.displacement = (-1, 0)
        elif key == DOWN_ARROW:
            self.displacement = (1, 0)
        elif key == ord('q'):
            exit()
        else:
            self.displacement = (0, 0)


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Invalid arguments!\nMust be [path_to_image]\n')
        exit()

    # load image
    image_path = sys.argv[1]
    #image_path = '/Users/alexey_bauman/projects/bionic_eye/test_images/rotated_rect.jpg'
    image = cv2.imread(image_path, flags=cv2.IMREAD_GRAYSCALE)


    # mechanical eye parameters
    mech_eye_params = {
        'field_size': 19
    }
    # opimal ganglions parameters
    ganglions_params = {
        'cells_type': 'on-center',
        'receptive_field_shape': (1, 4),
        'center_surround_tolerance': 'constant',
        'center_threshold': 0.8,
        'surround_threshold': 0.73
    }
    # optimal pvc parameters
    simple_pvc_params = {
        'receptive_field_size': 7,
        'regions_tolerance': 'linear',
        'on_region_threshold': 0.3,
        'off_region_threshold': 0.75
    }

    # create structural elements of eye model
    mech_eye = MechanicalEye(image=image, **mech_eye_params)
    receptors = RodsBinaryLayer2(data_source=mech_eye)
    ganglions = GanglionsBinaryLayer2(previous_layer=receptors, **ganglions_params)
    simple_pvcs = SimplePVCBinaryLayer2(previous_layer=ganglions, **simple_pvc_params)

    borders_map = BordersMap(mech_eye, ganglions)
    moving_decisions = MovingDecisions()

    # visualise initial state

    # mech eye
    mech_eye_img = cv2.cvtColor(mech_eye.image_n_frame, code=cv2.COLOR_RGB2BGR)
    mech_eye_img = cv2.resize(mech_eye_img, dsize=(0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Mechanical Eye', mech_eye_img)
    cv2.moveWindow('Mechanical Eye', MECH_EYE_WIN_X, MECH_EYE_WIN_Y)

    # frame
    ret, frame_img = cv2.threshold(mech_eye.frame, thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
    frame_img = cv2.resize(frame_img, dsize=(0, 0), fx=11, fy=11, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Frame', frame_img)
    cv2.moveWindow('Frame', FRAME_WIN_X, FRAME_WIN_Y)

    # ganglions' response
    ret, gangl_img = cv2.threshold(ganglions.response, thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
    gangl_img = cv2.resize(gangl_img, dsize=(0, 0), fx=19, fy=19, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Ganglion', gangl_img)
    cv2.moveWindow('Ganglion', GANGL_WIN_X, GANGL_WIN_Y)

    # simple pvcs' response
    for type_ in SIMPLE_PVC_TYPES:
        ret, simple_pvcs_img = cv2.threshold(simple_pvcs.response[type_], thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
        simple_pvcs_img = cv2.resize(simple_pvcs_img, dsize=(0, 0), fx=40, fy=40,
                                     interpolation=cv2.INTER_NEAREST)
        cv2.imshow(f'{type_}', simple_pvcs_img)

        if type_ == 'vertical':
            cv2.moveWindow(F'{type_}', PVC_VERTICAL_WIN_X, PVC_VERTICAL_WIN_Y)
        elif type_ == 'horizontal':
            cv2.moveWindow(F'{type_}', PVC_HORIZONTAL_WIN_X, PVC_HORIZONTAL_WIN_Y)
        elif type_ == 'left_inclined':
            cv2.moveWindow(F'{type_}', PVC_LEFT_WIN_X, PVC_LEFT_WIN_Y)
        elif type_ == 'right_inclined':
            cv2.moveWindow(F'{type_}', PVC_RIGHT_WIN_X, PVC_RIGHT_WIN_Y)

    # borders map
    ret, borders_map_img = cv2.threshold(borders_map.map, thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
    borders_map_img = cv2.resize(borders_map_img, dsize=(0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    cv2.imshow('Borders map', borders_map_img)
    cv2.moveWindow('Borders map', BORDERS_WIN_X, BORDERS_WIN_Y)

    cv2.waitKey(1)

    # start working
    n_iter = 0
    while True:
        n_iter += 1
        # perform one iteration
        mech_eye.move(moving_decisions.displacement)
        receptors.run()
        ganglions.run()
        simple_pvcs.run()
        borders_map.run()

        print(f"iter {n_iter}: {mech_eye.center_position}")

        # visualise current situation

        # mech eye
        mech_eye_img = cv2.cvtColor(mech_eye.image_n_frame, code=cv2.COLOR_RGB2BGR)
        mech_eye_img = cv2.resize(mech_eye_img, dsize=(0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Mechanical Eye', mech_eye_img)
        cv2.moveWindow('Mechanical_Eye', MECH_EYE_WIN_X, MECH_EYE_WIN_Y)

        # frame
        ret, frame_img = cv2.threshold(mech_eye.frame, thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
        frame_img = cv2.resize(frame_img, dsize=(0, 0), fx=11, fy=11, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Frame', frame_img)
        cv2.moveWindow('Frame', FRAME_WIN_X, FRAME_WIN_Y)

        # ganglions' response
        ret, gangl_img = cv2.threshold(ganglions.response, thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
        gangl_img = cv2.resize(gangl_img, dsize=(0, 0), fx=19, fy=19, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Ganglion', gangl_img)
        cv2.moveWindow('Ganglion', GANGL_WIN_X, GANGL_WIN_Y)

        # simple pvcs' response
        for type_ in SIMPLE_PVC_TYPES:
            ret, simple_pvcs_img = cv2.threshold(simple_pvcs.response[type_], thresh=0.5, maxval=255,
                                                 type=cv2.THRESH_BINARY)
            simple_pvcs_img = cv2.resize(simple_pvcs_img, dsize=(0, 0), fx=40, fy=40,
                                         interpolation=cv2.INTER_NEAREST)
            cv2.imshow(f'{type_}', simple_pvcs_img)

            if type_ == 'vertical':
                cv2.moveWindow(F'{type_}', PVC_VERTICAL_WIN_X, PVC_VERTICAL_WIN_Y)
            elif type_ == 'horizontal':
                cv2.moveWindow(F'{type_}', PVC_HORIZONTAL_WIN_X, PVC_HORIZONTAL_WIN_Y)
            elif type_ == 'left_inclined':
                cv2.moveWindow(F'{type_}', PVC_LEFT_WIN_X, PVC_LEFT_WIN_Y)
            elif type_ == 'right_inclined':
                cv2.moveWindow(F'{type_}', PVC_RIGHT_WIN_X, PVC_RIGHT_WIN_Y)

        # borders map
        ret, borders_map_img = cv2.threshold(borders_map.map, thresh=0.5, maxval=255, type=cv2.THRESH_BINARY)
        borders_map_img = cv2.resize(borders_map_img, dsize=(0, 0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('Borders map', borders_map_img)
        cv2.moveWindow('Borders map', BORDERS_WIN_X, BORDERS_WIN_Y)

        moving_decisions.run()






