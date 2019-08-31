"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
import picamera
# import pygame


# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.100', 8000))
connection = client_socket.makefile('wb')

# pygame.mixer.init()
# pygame.mixer.music.load("HORN4.wav")
# pygame.mixer.music.play()

try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)      # pi camera resolution
        camera.framerate = 10               # 10 frames/sec
        time.sleep(2)                       # give 2 secs for camera to initilize
        start = time.time()
        stream = io.BytesIO()

        # send jpeg format video stream
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start > 600:   # This line automatically kills the program after 10 min.
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
