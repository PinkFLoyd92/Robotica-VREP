try:
    import vrep
    import time

except:
    print('--------------------------------------------------------------')
    print('"vrep.py" could not be imported. This means very probably that')
    print('either "vrep.py" or the remoteApi library could not be found.')
    print('Make sure both are in the same folder as this file,')
    print('or appropriately adjust the file "vrep.py"')
    print('--------------------------------------------------------------')
    print('')

print('Program started')
vrep.simxFinish(-1) # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1', 19997, False, True, 5000, 5) # Connect to V-REP

def main():
    """Main function..."""

    errorCode,target=vrep.simxGetObjectHandle(clientID,'Quadricopter_target',vrep.simx_opmode_oneshot_wait)
    # Now try to retrieve data in a blocking fashion (i.e. a service call):

    while 1:
        x = float(input("ingrese x"))
        y = float(input("ingrese y"))
        z = float(input("ingrese z"))

        returnCode,position= vrep.simxGetObjectPosition(clientID, target, -1, vrep.simx_opmode_oneshot_wait)
        returnCode= vrep.simxSetObjectPosition(clientID, target, -1, [x, y, z], vrep.simx_opmode_oneshot_wait)

        print("Updated position")
        time.sleep(1)

if clientID != -1:
    print('Connected to remote API server')
    main()
else:
    print("No se pudo conectar...")


