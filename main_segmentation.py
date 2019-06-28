import numpy as np
import matplotlib.pyplot as plt
import cv2
import tensorflow_detection as tfd
import webbrowser
import sys

#script_dir = os.path.dirname(os.path.abspath('__file__'))
im = cv2.imread(str(sys.argv[1])+'.png')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
(_,contours, hierar) = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
count1=0
noiserem_con=[]
con_len1=len(contours)
# img1=255*np.ones(np.shape(imgray))
# cv2.drawContours(img1,contours,-1, (0,255,0), 3)
# cv2.imwrite('ppt.jpg',img1)
for i in range(con_len1):
    m, n, p = np.shape(contours[i])
    if(m>=10):
        if(hierar[0][i][3]==0):
            noiserem_con.append(0)
            count1=count1+1
            noiserem_con[count1-1]=contours[i]
# img1=255*np.ones(np.shape(imgray))
# cv2.drawContours(img1,noiserem_con,-1, (0,255,0), 3)
# cv2.imwrite('ppt_noiserem.jpg',img1)
con_len2=len(noiserem_con)
for i in range(1,con_len2):
    M1=cv2.moments(noiserem_con[i])
    ci=int(M1['m10']/M1['m00'])
    dum=i
    for j in range(i-1,-1,-1):
        M2=cv2.moments(noiserem_con[j])
        cj= int(M2['m10'] / M2['m00'])
        if(cj>ci):
            a=noiserem_con[i]
            noiserem_con[i]=noiserem_con[j]
            noiserem_con[j]=a
            i=i-1
    i=dum
#img2=255*np.ones(np.shape(imgray))
idx=0
dumy=''
for contour in noiserem_con:
    idx +=1
    [x,y,w,h1] = cv2.boundingRect(contour)
    # print x,y,w,h1
    roi=imgray[y:y+h1,x:x+w]
    # cv2.rectangle(imgray, (x, y), (x + w, y + h1), (255, 0, 255), 2)
    ret, thresh1 = cv2.threshold(roi, 127, 255, cv2.THRESH_BINARY)
    im1 = 255 * np.ones(((h1 + w),( w + h1)))
    im1[w/2:h1 + w/2, h1/2:w + h1/2] = thresh1
    resized_image = cv2.resize(im1, (45, 45))
    #print tfd.detection(resized_image)
    cv2.imwrite(str(idx)+'.jpg',resized_image)
    rec=tfd.detection(str(idx)+'.jpg')
    if rec=='plus':
        dumy=dumy+'%2B'
    elif rec=='div':
        dumy=dumy+'%2F'
    elif rec=='minus':
        dumy=dumy+'-'
    elif rec=='times':
        dumy=dumy+'*'
    else:
        dumy=dumy+rec

print dumy
url='https://www.wolframalpha.com/input/?i='
webbrowser.open(url+dumy)

# cv2.imwrite('bound.jpg',imgray)
# cv2.waitKey(0)
