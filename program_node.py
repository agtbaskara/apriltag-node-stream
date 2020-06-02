# run this program on each RPi to send a labelled image stream
import socket
import time
from imutils.video import VideoStream
import imagezmq
import cv2

server_address = "tcp://127.0.0.1:5555"

sender = imagezmq.ImageSender(connect_to=server_address)
node_name = socket.gethostname() # send RPi hostname with each image
camera = VideoStream().start()

time.sleep(2.0)  # allow camera sensor to warm up
print("Start Stream")

while True:  # send images as stream until Ctrl-C
    image = camera.read()
    image = cv2.resize(image, (640,480))
    sender.send_image(node_name, image)