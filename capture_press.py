'''
author:peter
time:2018.8.7
function:实现视频实时抓拍，按s拍摄当前相机图片，按q退出
'''

from PIL import Image
import select
import v4l2capture
import numpy as np
import sys
import os
import cv2 as cv
import shutil
import time
import pygame.camera as camera

camera.init()
cams = camera.list_cameras()

# Open the video device.
num=sys.argv[1]
val =int(sys.argv[2])
video = v4l2capture.Video_device(cams[int(num)])
# config 
video.set_exposure_auto(1)
video.set_exposure_absolute(val)
video.set_auto_white_balance(1)
#video.set_white_balance_temperature(4600)
#video.set_focus_auto(1)
size_x, size_y = video.set_format(3264, 2448,fourcc='MJPG')

dpath = "press_save"+num

if not os.path.exists(dpath):
    os.mkdir(dpath)
'''
if os.path.exists(dpath):
    shutil.rmtree(dpath)
    os.mkdir(dpath)
else:
    os.mkdir(dpath)
'''

video.create_buffers(1)
video.queue_all_buffers()
video.start()
start = time.time()
cv.namedWindow("video"+num,cv.WINDOW_NORMAL)
index = 1
while True:
    select.select((video,), (), ())
    image_data = video.read_and_queue()
    frame = cv.imdecode(np.frombuffer(image_data,dtype=np.uint8),cv.IMREAD_COLOR)
    cv.imshow('video'+num,frame)
    fname = dpath+'/'+str(index)+'.jpg'
    #cv.imwrite(fname,frame)
    key=cv.waitKey(10)
    if key&0xff == ord('s'):
        cv.imwrite(fname,frame)
        counts = len(os.listdir(dpath))
        print("{} --> saveing {}th image".format(dpath,counts))
        index+=1
    if key&0xff == ord('q'):
        break
    

end =time.time()
cost_time = end-start

counts = len(os.listdir(dpath))
print("SUM:{} --> save {} images".format(dpath,counts))

video.close()
cv.destroyAllWindows()


