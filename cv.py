# -*- coding: utf-8 -*-
"""
Created on Thu Feb 09 21:38:25 2017

@author: Juan
"""

import vrep
import cv2
import numpy
import array
from PIL import Image as I
import time

def detectar(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_green = numpy.array([40,70,70])
    upper_green = numpy.array([80,256,256])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = numpy.ones((5, 5), numpy.uint8)
    erosion = cv2.erode(mask, kernel)
    cv2.imshow('erosion', erosion)
    dilatacion = cv2.dilate(erosion, kernel, iterations=1)
    cv2.imshow('dilatacion', dilatacion)
    img2, contorno, jerarquia = cv2.findContours(dilatacion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contorno, -1, (0, 0, 0), 2)
    return img, len(contorno)
    #print "lista de contornos: " + str(len(contorno))

vrep.simxFinish(-1)

clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

if clientID!=-1:
    print 'Connected to remote API server'
    
    # get vision sensor objects
    
    res, cam0 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor0', vrep.simx_opmode_oneshot_wait)
    print res
    print cam0
    res, cam1 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor1', vrep.simx_opmode_oneshot_wait)
    
    res, target = vrep.simxGetObjectHandle(clientID, 'Quadricopter_target', vrep.simx_opmode_oneshot_wait)
    
    err, resolution, image = vrep.simxGetVisionSensorImage(clientID, cam0, 0, vrep.simx_opmode_oneshot_wait)
    
    verr, linear, angular = vrep.simxGetObjectVelocity(clientID, target, vrep.simx_opmode_streaming)
    print err
    cont = 0
    detect = 0
    mov=0
    
    while (vrep.simxGetConnectionId(clientID) != -1):
        # get image from vision sensor 'v0'
        err, resolution, image = vrep.simxGetVisionSensorImage(clientID, cam0, 0, vrep.simx_opmode_oneshot_wait)
        if err == vrep.simx_return_ok:
            image_byte_array = array.array('b', image)
            image_buffer = I.frombuffer("RGB", (resolution[0],resolution[1]), image_byte_array, "raw", "RGB", 0, 1)
            img2 = numpy.asarray(image_buffer)
            processed, de = detectar(img2)
            
            if de > detect:
                cont=cont+1
            detect=de            
                        
            img2 = processed.ravel()
            vrep.simxSetVisionSensorImage(clientID, cam1, img2, 0, vrep.simx_opmode_oneshot)
            
            verr, linear, angular = vrep.simxGetObjectVelocity(clientID, target, vrep.simx_opmode_buffer)
            
            lin= linear[0]*linear[0]+linear[1]*linear[1]+linear[2]*linear[2]
            if lin>0:
                mov = time.time()
            elif mov>0:
                if time.time() - mov > 3:
                    break
            
        elif err == vrep.simx_return_novalue_flag:
            print "no image yet"
        #else:
            #print err
    
    print 'Objetos encontrados:'
    print cont
        
        


else:
    print 'Cannot connect to remote API server'
