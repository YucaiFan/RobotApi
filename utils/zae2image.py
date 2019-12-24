#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import with_statement # for python 2.5

import sys
from optparse import OptionParser

try:
    import openravepy
except ImportError:
    print "openravepy is not set into PYTHONPATH env variable, attempting to add"
    # use openrave-config to get the correct install path
    from subprocess import Popen, PIPE
    try:
        openrave_config = Popen(['openrave-config','--python-dir'],stdout=PIPE)
        openravepy_path = openrave_config.communicate()
        if openrave_config.returncode != 0:
            raise OSError('bad args')
            
        sys.path.append(openravepy_path[0].strip())
    except OSError:
        import os, platform
        from distutils.sysconfig import get_python_lib
        if sys.platform.startswith('win') or platform.system().lower() == 'windows':
            # in windows so add the default openravepy installation
            allnames = os.listdir('C:\\Program Files')
            possibledirs = [os.path.join('C:\\Program Files',name) for name in allnames if name.startswith('openrave')]
            if len(possibledirs) > 0:
                sys.path.append(get_python_lib(1,prefix=possibledirs[0]))
    import openravepy

from openravepy import *
import time

def get_image(filename):
    #RaveInitialize(False, DebugLevel.Fatal) # don't want any spurious text
    #RaveLoadPlugin('qtcoinrave') # optional for IV/VRML file reading?
    env=Environment()
    #env.StopSimulation() # don't want another thread distributing things
    env.SetViewer('qtcoin')
    try:
        if filename is not None:
            robot=env.ReadRobotXMLFile(filename,atts={'skipgeometry':'1'})
            env.Add(robot)
            time.sleep(1)

            env.GetViewer().sendCommand('SetFiguresInCamera 1')
            I = env.GetViewer().GetCameraImage(640,480,  env.GetViewer().GetCameraTransform(),[640,640,320,240])
            scipy.misc.imsave('openrave.jpg',I)

    finally:
        env.Destroy()
        
    return 0

if __name__ == '__main__':
    get_image("../data/examples/kawada-hironx.zae")

    print("="*20)
