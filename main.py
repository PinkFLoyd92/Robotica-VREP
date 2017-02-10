# try:
#     import vrep
#     import time
#     import numpy as np
#     import cv2

# except:
#     print('--------------------------------------------------------------')
#     print('"vrep.py" could not be imported. This means very probably that')
#     print('either "vrep.py" or the remoteApi library could not be found.')
#     print('Make sure both are in the same folder as this file,')
#     print('or appropriately adjust the file "vrep.py"')
#     print('--------------------------------------------------------------')
#     print('')

# print('Program started')
# vrep.simxFinish(-1) # just in case, close all opened connections
# clientID = vrep.simxStart('127.0.0.1', 19997, False, True, 5000, 5) # Connect to V-REP

# def main():
#     """Main function..."""

#     errorCode, target = vrep.simxGetObjectHandle(clientID, 'Quadricopter_target', vrep.simx_opmode_oneshot_wait)
#     errorCode, sensor = vrep.simxGetObjectHandle(clientID, 'Quadricopter_floorCamera', vrep.simx_opmode_oneshot_wait)
#     print(sensor)
#     err, resolution, image = vrep.simxGetVisionSensorImage(clientID, sensor, 0, vrep.simx_opmode_streaming)
#     # Now try to retrieve data in a blocking fashion (i.e. a service call):

#     while 1:
#         err, resolution, image = vrep.simxGetVisionSensorImage(clientID, sensor, 0, vrep.simx_opmode_buffer)
#         if err == vrep.simx_return_ok:
#             img = np.array(image, dtype=np.uint8)
#             img.resize([resolution[0], resolution[1],3])
#             cv2.imshow('image', img)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         elif err == vrep.simx_return_novalue_flag:
#             print("no image yet")
#             pass
#         else:
#             print(err)


# if clientID != -1:
#     print('Connected to remote API server')
#     main()
# else:
#     print("No se pudo conectar...")

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 05 15:01:58 2015

@author: ACSECKIN
"""

# import vrep
# import time
# import cv2
# import numpy as np

# vrep.simxFinish(-1)

# clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)

# if clientID!=-1:
#     print 'Connected to remote API server'
#     print 'Vision Sensor object handling'
#     res, v1 = vrep.simxGetObjectHandle(clientID, 'Quadricopter_frontCamera', vrep.simx_opmode_oneshot_wait)
#     print 'Getting first image'
#     err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_streaming)
#     while (vrep.simxGetConnectionId(clientID) != -1):
#         err, resolution, image = vrep.simxGetVisionSensorImage(clientID, v1, 0, vrep.simx_opmode_buffer)
#         if err == vrep.simx_return_ok:
#             print "image OK!!!"
#             img = np.array(image,dtype=np.uint8)
#             img.resize([resolution[1],resolution[0],3])
#             cv2.imshow('image',img)
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
#         elif err == vrep.simx_return_novalue_flag:
#             print "no image yet"
#             pass
#         else:
#           print err
# else:
#   print "Failed to connect to remote API Server"
#   vrep.simxFinish(clientID)

# cv2.destroyAllWindows()
import sys
import vrep
import time
import cv2
import numpy as np

print('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID != -1:
    print('Connected to remote API server')
    res, v0 = vrep.simxGetObjectHandle(clientID, 'Vision_sensor',
                                       vrep.simx_opmode_oneshot_wait)
    print(v0)

    res, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0,
                                                           int(sys.argv[1]), vrep.simx_opmode_streaming)

    time.sleep(2)
    print(res)
    while (vrep.simxGetConnectionId(clientID)!=-1):
        res, resolution, image = vrep.simxGetVisionSensorImage(clientID, v0, 0, vrep.simx_opmode_buffer)
        if res == vrep.simx_return_ok:
            print "success."
            img = np.array(image, dtype=np.uint8)
            img.resize([resolution[1], resolution[0], 3])
            cv2.imshow('image', img)
            cv2.waitKey(1)
        else:
            print(res)
            print(resolution)
            time.sleep(1)
    vrep.simxFinish(clientID)
else:
    print 'Failed connecting to remote API server'
print 'Program ended'
