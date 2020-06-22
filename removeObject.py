#remove_object but python
import json
import sys
import cv2 as cv
import numpy as np

if len(sys.argv) != 4:
    print("Correct format is:")
    print("python removeObject.py JSONfileName JPGfileName objectToRemove")
else:
    jsonFileName = sys.argv[1]
    jpgFileName = sys.argv[2]
    objectName = sys.argv[3]
    #open file
    openFile = open(jsonFileName, "r")
    pyJson = json.load(openFile)
    openFile.close()
    #pull points for object to change
    #list of dicts
    shapesDict = pyJson['shapes']
    #list of Dicts with label:objectName   
    objectDict = [d for d in shapesDict if objectName in d.values()]
    for d in objectDict:
        #list of coordinates [x,y]
        listPoints = d['points']
        npPoints = np.array([listPoints], dtype=np.int32)
        img = cv.imread(jpgFileName, cv.IMREAD_COLOR)
        #listPoints needs to be a numpy array
        #newImage = cv.fillPoly(img, npPoints, (255, 255, 255))
        cv.fillPoly(img, npPoints, 255)
        #print(newImage)