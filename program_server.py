# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq
from pupil_apriltags import Detector

fx = 472.13107208
fy = 472.3044311
cx = 322.23325564
cy = 238.25801953
tag_size = 0.055

camera_params = ([fx, fy, cx, cy])

at_detector = Detector(families='tag36h11',
                       nthreads=1,
                       quad_decimate=1.0,
                       quad_sigma=0.0,
                       refine_edges=1,
                       decode_sharpening=0.25,
                       debug=0)

image_hub = imagezmq.ImageHub()

while True:  # show streamed images until Ctrl-C
    node_name, img = image_hub.recv_image()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    tags = at_detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=tag_size)

    if len(tags):
        print("Rotation Matrix:")
        print(tags[0].pose_R)
        print("Translation Matrix:")
        print(tags[0].pose_t)
        # Draw Bounding Box
        corner0 = (int(tags[0].corners[0][0]), int(tags[0].corners[0][1]))
        corner1 = (int(tags[0].corners[1][0]), int(tags[0].corners[1][1]))
        corner2 = (int(tags[0].corners[2][0]), int(tags[0].corners[2][1]))
        corner3 = (int(tags[0].corners[3][0]), int(tags[0].corners[3][1]))
        img = cv2.line(img, corner0, corner1, (180, 105, 255), 5)
        img = cv2.line(img, corner1, corner2, (180, 105, 255), 5)
        img = cv2.line(img, corner2, corner3, (180, 105, 255), 5)
        img = cv2.line(img, corner3, corner0, (180, 105, 255), 5)
        
    cv2.imshow(node_name, img) # 1 window for each RPi
    cv2.waitKey(1)

    image_hub.send_reply(b'OK')
    