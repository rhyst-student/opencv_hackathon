import numpy as np
import cv2
import imutils
#from matplotlib import pyplot as plt
import time


global sift
sift = cv2.SIFT_create(nfeatures=1000000)
global bf
bf = cv2.BFMatcher(cv2.NORM_L2)


class testImage():
    def __init__(self, imageName, imageFile, minMatches = 30, colour = (255,0,0), Lratio = 0.75, minArea = 200, blur = 7, show = False):
        self.name = imageName
        self.image = 0
        self.minMatches = minMatches
        self.colour = colour
        self.Lratio = Lratio
        self.minArea = minArea
        self.img_features = 0
        self.img_des = 0
        self.lastIdentified_time = time.time()
        self.lastIdentified_frame = 0
        self.loadImage(imageFile, blur)
        self.findFeatures()
        if show == True:
            cv2.imshow(imageName,self.image)
            print("press any key to continue")
            cv2.waitKey(0)
            cv2.destroyWindow(imageName)
            

    def loadImage(self, imageFile, blur):
        self.image = cv2.imread(imageFile,1)
        #print(imageFile)
        cv2.imshow('test',self.image)
        cv2.waitKey(0)
        #self.image = imutils.resize(self.image, width = 700)
        self.image = cv2.medianBlur(self.image,blur)
        cv2.imshow('test',self.image)
        cv2.waitKey(0)
    
    def findFeatures(self):
        features, des = sift.detectAndCompute(self.image, None)
        self.img_features = features
        self.img_des = des

class trainVideo():
    def __init__(self, videoFile):
        self.feed = 0
        self.image = 0
        self.img_features = 0
        self.img_des = 0
        self.loadVideo(videoFile)

    def loadVideo(self, videoFile):
        self.feed = cv2.VideoCapture(videoFile)

    def findFeatures(self):
        features, des = sift.detectAndCompute(self.image, None)
        self.img_features = features
        self.img_des = des
        if features == []:
            cv2.imshow('test', self.image)
            cv2.waitKey(0)

    def nextFrame(self,checkRet = 1):
        ret, frame = self.feed.read()
        #cv2.imshow("testing", frame)
        #cv2.waitKey(0)
        #print(self.feed)
        count = 0
        while (ret == 0) or (type(frame) == type(None)):
            if (checkRet == 1):
                print("failed or end of file, dont know tbh")
                #self.feed.release()
                cv2.waitKey(0)
                #cv2.destroyAllWindows()
                #exit(0)
            if (count > 30):
                print("could not read an input within 30 tries")
                self.feed.release()
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                exit(0)
            count += 1
            ret, frame = self.feed.read()
        self.image = frame
        self.findFeatures()
        

def match_feature(query, train, debug = 0): 
    # finds matches between features
    #print(train.img_des)
    if len(train.img_features) == 0:
        return 3     # no features detected
    try: 
        matches = bf.knnMatch(query.img_des, train.img_des, k = 2)
    except:
        print("---error---")
        print(train.img_features)
        print(train.img_des)
        print("-----------")
        return 2
    # Nearest neighbour ratio test to find good matches
    good = []       
    matches = [match for match in matches if len(match) == 2] 
    for m, n in matches:
        if m.distance < query.Lratio * n.distance:                                                               
            good.append(m)
         
    if len(good) >= query.minMatches:
        # Draw a polygon around the recognized object
        src_pts = np.float32([query.img_features[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([train.img_features[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        
        # Get the transformation matrix
        M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
               
        # Find the perspective transformation to get the corresponding points
        h, w = query.image.shape[:2]
        pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
        try:
            dst = cv2.perspectiveTransform(pts, M)
        except:
            return 2    # some sort of error???
        if (PolygonArea(dst) > query.minArea):                                                                     
            train.image = cv2.polylines(train.image, [np.int32(dst)], True, query.colour, 2, cv2.LINE_AA)
            #print(" - identified:",query.name)                                                                
            return 0    # detected somehting
        return 1        # didnt detect anything


def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0][0] * corners[j][0][1]
        area -= corners[j][0][0] * corners[i][0][1]
    area = abs(area) / 2.0
    return area


## main
# create test image objects
def main():
    imageList = ['piBox1','bambooBox1']
    colourList = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255),(125,0,0),(0,125,0),(0,0,125),(125,125,0),(125,0,125),(0,125,125)]

    testImages = []
    for i in range(len(imageList)):
        testImages.append(testImage(imageList[i],'images/{}.jpg'.format(imageList[i]),colour = colourList[i], show = False))

    # main loop
    video = trainVideo('images/findVideo2.mp4')
    frameCount = 0
    while True:
        #print('mainloop')
        print("frame {}".format(frameCount))
        frameCount += 1
        video.nextFrame(0)
        found = []
        for i in range(len(testImages)):
            error = match_feature(testImages[i], video)
            if error == 0:
                testImages[i].lastIdentified_time = time.time()
                testImages[i].lastIdentified_frame = frameCount
                found.append(i)
        
        cv2.imshow("result", video.image)
        print("-"*10)
        for i in testImages:
            print("{} last identified at {}:{} (frame {})".format(i.name, time.localtime(i.lastIdentified_time).tm_hour, time.localtime(i.lastIdentified_time).tm_min, i.lastIdentified_frame))
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break   
    video.feed.release()
    cv2.destroyAllWindows()

main()
input()
