import numpy as np
import cv2
import csv

import os

import glob



def get_dominant_color(height,width,color):
    bar=np.zeros((height,width,3),np.uint8)
    bar[:]=color
    red,green,blue=int(color[2]),int(color[1]),int(color[0])
    return bar,(red,green,blue)






# Read the image
img_path='../assets/2jpg.jpg'
img=cv2.imread(img_path)



# extract the height, width and the number of channels of the image
height,width,_=np.shape(img)

# print(height,width)

# reshape the image to a 2D array of pixels and 3 color values (RGB)
# The line `data=np.reshape(img,(height*width,3))` is reshaping the image data from a 3D array
# (representing the image with height, width, and channels) into a 2D array of pixels and 3 color
# values (RGB).
data=np.reshape(img,(height*width,3))

# The line `data=np.float32(data)` is converting the data array to a floating-point data type. In
# OpenCV, it is common to perform calculations and operations on images using floating-point data
# types for better precision and accuracy. By converting the data array to `np.float32`, you are
# ensuring that the data is in a format that is suitable for certain image processing operations that
# require floating-point values.
data=np.float32(data)


# clustering
number_of_clusters=5
# The line `criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)` is setting the
# criteria for the k-means clustering algorithm used in the code. Here's what each part of the
# criteria tuple represents:
criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
# The line `flags=cv2.KMEANS_RANDOM_CENTERS` in the code is setting the flag for the k-means
# clustering algorithm used in OpenCV. Specifically, `cv2.KMEANS_RANDOM_CENTERS` is a flag that
# indicates the method for initializing the initial cluster centers in the k-means algorithm.
flags=cv2.KMEANS_RANDOM_CENTERS

# The line `compactness, labels, centers = cv2.kmeans(data, number_of_clusters, None, criteria, 10,
# flags)` is performing the k-means clustering algorithm on the image data. Here's a breakdown of what
# each part of this line does:
compactness,labels,centers=cv2.kmeans(data,number_of_clusters,None,criteria,10,flags)

# print(centers)
font=cv2.FONT_HERSHEY_SIMPLEX

bars=[]
rgb_values=[]

for index,row in enumerate(centers):
    bar,rgb=get_dominant_color(200,200,row)
    bars.append(bar)
    rgb_values.append(rgb)
img_bar=np.hstack(bars)  


# csv data
csv_data=[]
for index, row in enumerate(rgb_values):
    image=cv2.putText(img_bar,f'{index+1}. RGB: {row}',(5+200*index,200-10),font,0.5,(255,0,0),1,cv2.LINE_AA)
    print(f'{index+1}. RGB{row}')
    # for i in range(len(row)):
        # print(row[i])
    # csv_data.append([index+1, row,img_path])




# write to csv
# with open('dominant_colors.csv','w',newline='') as file:
#     writer=csv.writer(file)
#     writer.writerow(['Index','Red','Image'])
#     writer.writerows(csv_data)


# open the image

cv2.imshow('image',img)

# domain color
cv2.imshow('dominant colors',img_bar)

# wait for a key to be pressed
cv2.waitKey(0)
