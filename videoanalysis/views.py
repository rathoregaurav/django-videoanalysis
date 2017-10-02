# -*- coding: utf-8 -*-
from django.shortcuts import render
import cv2
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.response import Response
from tvid.settings import STATIC_URL
from rest_framework import status
import subprocess

def getDirectoryContents(dPath):
    import os 
    lst = []
    for sChild in os.listdir(dPath):                
        sChildPath = os.path.join(dPath,sChild)
        if os.path.isdir(sChildPath):
            getDirectoryContents(sChildPath)
        else:
            lst.append(sChildPath)
    del lst[0]
    return lst

def getVideoFrames(ipath, vpath):
    vidcap = cv2.VideoCapture(vpath)
    # vidcap.set(cv2.CAP_PROP_POS_MSEC,1000)
    success,image = vidcap.read()
    print success
    seconds = 10
    fps = int(round(vidcap.get(cv2.CAP_PROP_FPS))) # Gets the frames per second
    print "fps: "+str(fps)

    multiplier = fps * seconds
    length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    print "length: "+str(length)
    total_dr = length/fps
    print "total_dr: "+str(total_dr)
    interval = 30
    count = 0
    success = True

#     while success:
#     #     success,image = vidcap.read()
#     #     if count%interval==0:
#     #         cv2.imwrite("frames/frame%d.jpg" % count, image)     # save frame as JPEG file
#     #     count += 1
#         frameId = int(round(vidcap.get(1))) #current frame number, rounded b/c sometimes you get frame intervals which aren't integers...this adds a little imprecision but is likely good enough
#         success, image = vidcap.read()
#         if frameId % fps == 0:
#             cv2.imwrite(ipath+""+"/frame%d.jpg" % frameId, image)

    for i in range(length):
        success, image = vidcap.read()
        if i%fps==0:
            cv2.imwrite(ipath+""+"/frame%d.jpg" % i, image)
    vidcap.release()    
    return total_dr


def getImageWithFaces(ipath, vpath):
    total_video_duration = "None"
    t1 = datetime.now()
    total_video_duration = getVideoFrames(ipath, vpath)
    t2 = datetime.now()
    # imagePath = sys.argv[1]
    count=0
    t3 = datetime.now()
    lst = getDirectoryContents(ipath)
    cascPath = STATIC_URL+'/xml/haarcascade_frontalface_default.xml'
    faceCascade = cv2.CascadeClassifier(cascPath)
    for path in lst:
        imagePath = path
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        if len(faces)!=0:
            count+=1
    t4 = datetime.now()
    print t4-t3
    return [count, total_video_duration]


@api_view(["POST", "GET"])
@permission_classes((permissions.AllowAny,))
def videoAnalyze(request):
    try:
        t1=datetime.now()
        # ipath = "/Users/gaurav/AnacondaProjects/FD/frames"
        # vpath = "/Users/gaurav/AnacondaProjects/FD/naja.mp4"
        # ipath = "/Users/gaurav/Documents/cc"
        # vpath = "/Users/gaurav/Documents/cc.mp4"
        ipath = request.data["ipath"]
        vpath = request.data["vpath"]
        data = getImageWithFaces(ipath, vpath)
        total_face_duration = data[0]
        total_video_duration = data[1]
        t2=datetime.now()

            # Draw a rectangle around the faces
            # for (x, y, w, h) in faces:
            #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # cv2.imshow("Faces found", image)
            # cv2.waitKey(0)
        return Response({"success": True, "total_video_duration": total_video_duration, "total_face_duration": total_face_duration}, status = status.HTTP_200_OK)
    except Exception as e:
        print e
        return Response({"success": False, "error": str(e)}, status=status.HTTP_404_NOT_FOUND)
