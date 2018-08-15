import cv2
import sys

numberOfCabins=4
imagePath = "c04.jpg"
cascPath = "haarcascade_frontalface_default.xml"

faceCascade = cv2.CascadeClassifier(cascPath)

image = cv2.imread(imagePath)
height, width, channels = image.shape
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
        elif cabin["isCabinFull"] == False:
            print "Cabin No: "+str(cabin["cabinNumber"]+1)+" is Empty."
# print cabinChunk


