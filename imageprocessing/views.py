# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser, MultiPartParser
from rest_framework import status
import inflect
import cv2
import sys
from tvid.settings import BASE_DIR, MEDIA_ROOT, STATIC_URL

print BASE_DIR


class CabinAnalyze(APIView):
    """
    form data:
    {
    "numberOfCabins": numberOfCabins,
    "imagePath": ""
    }
    """
    parser_classes = (MultiPartParser, FileUploadParser)
    def post(self, request, format=None):
        try:
            postData = request.data
            imagePath = postData["imagePath"]
            imagePath = str(MEDIA_ROOT)+"images/"+str(dict(request.FILES)["imagePath"][0].name)
            # print imagePath
            numberOfCabins = int(postData["numberOfCabins"])
            cascPath = str(STATIC_URL)+str("xml/haarcascade_frontalface_default.xml")
            # numberOfCabins=4
            # imagePath = "c04.jpg"
            faceCascade = cv2.CascadeClassifier(cascPath)
            image = cv2.imread(imagePath)
            height, width, channels = image.shape
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print height, width, channels

            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
                #flags = cv2.cv.CV_HAAR_SCALE_IMAGE
            )

            print("Found {0} faces!".format(len(faces)))
            print faces
            print height, width, channels

            # # Draw a rectangle around the faces
            # for (x, y, w, h) in faces:
            #     #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #     print x,y,w,h

            # cv2.imshow("Faces found", image)
            # # cv2.waitKey(0)

            # print len(faces)
            # print width
            cabinSpace = width/numberOfCabins
            totalCabins = numberOfCabins

            cabinChunk = []
            for i in range(numberOfCabins):
                cabin = []
                cabinInfo = {}
                cabinStart = cabinSpace*i
                cabinEnd = cabinSpace*(i+1)
                cabin.append(cabinStart)
                cabin.append(cabinEnd)
                cabinInfo["cabinLocation"] = cabin
                cabinInfo["isCabinFull"] = True
                cabinInfo["cabinNumber"] = i
                cabinChunk.append(cabinInfo)    
                
            # if len(faces)<numberOfCabins:
            if True:
                cabinStatus = []
                for cabin in cabinChunk:
                    returnDict = {}
                    cabinInfoBool = []
                    for i in faces:
                        if i[0] in range(cabin["cabinLocation"][0], cabin["cabinLocation"][1]):
                            cabinInfoBool.append(True)
                        else:
                            cabinInfoBool.append(False)
                    temp = False
                    for i in cabinInfoBool:
                        temp = i or temp
                    cabin["isCabinFull"] = temp
                    if cabin["isCabinFull"] == True:
                        print "Cabin No: "+str(cabin["cabinNumber"]+1)+" is Full."
                        result = "Cabin No: "+str(cabin["cabinNumber"]+1)+" is Full."
                        
                        returnDict["cabinNumber"] = inflect.engine().number_to_words(str(cabin["cabinNumber"]+1))
                        returnDict["isCabinFull"] = True
                        returnDict["result"] = result
                        cabinStatus.append(returnDict)

                    elif cabin["isCabinFull"] == False:
                        print "Cabin No: "+str(cabin["cabinNumber"]+1)+" is Empty."
                        result = "Cabin No: "+str(cabin["cabinNumber"]+1)+" is Empty."
                        returnDict["cabinNumber"] = inflect.engine().number_to_words(str(cabin["cabinNumber"]+1))
                        returnDict["isCabinFull"] = False
                        returnDict["result"] = result
                        cabinStatus.append(returnDict)

            # print cabinChunk

            return Response({"success": True, "data": cabinStatus})
        except Exception as e:
            print e
            return Response({"success": True, "data": str(e)})


