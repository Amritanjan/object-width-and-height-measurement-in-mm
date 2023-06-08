import cv2
import os
import numpy as np
import imutils
import cv2 as cv
import requests




url='http://192.168.43.1:8080/shot.jpg'

def convert_pix_to_cm(a):
    print(a)
    x=round(a*0.0145,2)
    return(x)


while(1):
    RawData = requests.get(url,verify=1)
    #print (RawData.status_code)
    #frame=cv2.imread("/home/amritanjan/Downloads/sugar/compreshed_img/test.jpg")
    if(RawData.status_code!=401):
    #if(frame is not None):
        One_D_Arry = np.array(bytearray(RawData.content),dtype=np.uint8)
        frame=cv.imdecode(One_D_Arry,-1)

        resized = imutils.resize(frame, width=900)
        output_img=resized.copy()
        gray=cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        (ret, thresh) = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        

        kernel = np.ones((3, 3), np.uint8)

        img_dilation = cv2.dilate(thresh, kernel, iterations=1)
        img_erosion = cv2.erode(img_dilation, kernel, iterations=1)

        cnt, _ = cv2.findContours(img_erosion.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in cnt:
            area=cv2.contourArea(c)
            if(area>100):
                x,y,w,h = cv2.boundingRect(c)
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                w=convert_pix_to_cm(w)
                h=convert_pix_to_cm(h)
                cv2.drawContours(output_img,[box],0,(0,0,255),1)
                cv2.drawContours(output_img,[c],-1,(0,255,0),1)
                output_img = cv2.putText(output_img, str(w)+"-"+str(h), (int(x),int(y)), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,0), 1, cv2.LINE_AA, False)
                #cv2.drawContours(output_img,[c],-1,(0,0,255),2)


        cv2.imshow("img",resized)
        cv2.imshow("output_img",output_img)

        key=cv2.waitKey(1)
        if key == ord('q'):
            break