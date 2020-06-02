import cv2
import glob
from pupil_apriltags import Detector

fx = 472.13107208
fy = 472.3044311
cx = 322.23325564
cy = 238.25801953
tag_size = 0.07

camera_params = ([fx, fy, cx, cy]) 

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

images = glob.glob('./sample_data/*.jpg')
for fname in images:
    img = cv2.imread(fname)
    img = cv2.resize(img, (640,480))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    tags = at_detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=tag_size)

    print(tags)