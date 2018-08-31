import cv2
import numpy as np

SPACE_KEY = 0x31
ENTER_KEY = 0x4C
Q_KEY = 0x0C

img_path = '/Users/alexey_bauman/projects/bionic_eye/test_images/rotated_rect.jpg'
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

"""windows = ['Mechanical Eye', 'Frame', 'Ganglions response', 'Simple V1 response', 'Borders Map']

for win_name in windows:
    cv2.namedWindow(win_name)
    key = cv2.waitKey(1)
    #cv2.resizeWindow(win_name, 1000, 1000)

for win_name in windows:
    cv2.imshow(win_name, img)
    key = cv2.waitKey(1)

key = cv2.waitKey(-1)
if key & 0xFF == Q_KEY:
    cv2.destroyAllWindows()
"""
win_name = 'Window 1'

cv2.namedWindow(win_name, flags=cv2.WINDOW_NORMAL)
cv2.resizeWindow(win_name, 400, 400)
key = cv2.waitKey(1000)

cv2.imshow(win_name, img)
cv2.resizeWindow(win_name, 400, 400)
key = cv2.waitKey(1)

cv2.moveWindow(win_name, 100, 100)


while key & 0xFF != ord('q'):
    key = cv2.waitKey(0)
cv2.destroyAllWindows()