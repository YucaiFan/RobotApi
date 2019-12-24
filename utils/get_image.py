from openravepy import *
import scipy
import time
env = Environment() # create openrave environment
env.SetViewer('qtcoin')
env.Load('../cmu-permma/cmu-permma.dae') # load a simple scene
time.sleep(1) # wait for viewer to initialize

env.GetViewer().SendCommand('SetFiguresInCamera 1') # also shows the figures in the image
I = env.GetViewer().GetCameraImage(640,480,  env.GetViewer().GetCameraTransform(),[640,640,320,240])
scipy.misc.imsave('openrave.jpg',I)
