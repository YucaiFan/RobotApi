#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009-2012 Rosen Diankov (rosen.diankov@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import with_statement # for python 2.5
__author__ = 'Rosen Diankov'
__copyright__ = 'Copyright (C) 2009-2010 Rosen Diankov (rosen.diankov@gmail.com)'
__license__ = 'Apache License, Version 2.0'

import sys
from optparse import OptionParser

__builtins__.__openravepy_version__ = '0.26'

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

def parse_robot(filename):
    RaveInitialize(False, DebugLevel.Fatal) # don't want any spurious text
    RaveLoadPlugin('qtcoinrave') # optional for IV/VRML file reading?
    env=Environment()
    env.StopSimulation() # don't want another thread distributing things
    try:
        if filename is not None:
            robot=env.ReadRobotXMLFile(filename,atts={'skipgeometry':'1'})
            env.Add(robot)

            res = []
            for m in robot.GetManipulators():
                res_dict = {}
                armindices = [i for i in m.GetArmIndices()]
                gripperindices = [i for i in m.GetGripperIndices()]
                # armindices = ','.join(str(i) for i in m.GetArmIndices())
                # gripperindices = ','.join(str(i) for i in m.GetGripperIndices())

                rows = ['name','base','end','arm-dof','gripper-dof','arm','gripper']
                val =  [m.GetName(),m.GetBase().GetName(),m.GetEndEffector().GetName(),str(len(m.GetArmIndices())),str(len(m.GetGripperIndices())),armindices,gripperindices]
                for i in range(len(rows)):
                    res_dict[rows[i]] = val[i]
                res.append(res_dict)
            return res # res is a list of dicts


            #elif options.doinfo.startswith('sensor'):
            #    robot=env.ReadRobotXMLFile(args[0],atts={'skipgeometry':'1'})
            #    env.Add(robot)
            #    rows = [['name','type','link']]
            #    for s in robot.GetAttachedSensors():
            #        rows.append([s.GetName(),str(s.GetSensor()),s.GetAttachingLink().GetName()])
            #    rows.append(rows[0])
            #    colwidths = [max([len(row[i]) for row in rows]) for i in range(len(rows[0]))]
            #    for i,row in enumerate(rows):
            #        print ' '.join([row[j].ljust(colwidths[j]) for j in range(len(colwidths))])
            #        if i == 0 or i == len(rows)-2:
            #            print '-'*(sum(colwidths)+len(colwidths)-1)
            #elif options.doinfo.startswith('link'):
            #    env.Load(args[0],{'skipgeometry':'1'})
            #    body=env.GetBodies()[0]
            #    rows = [['name','index','parents']]
            #    for link in body.GetLinks():
            #        rows.append([link.GetName(),str(link.GetIndex()),','.join(l.GetName() for l in link.GetParentLinks())])
            #    rows.append(rows[0])
            #    colwidths = [max([len(row[i]) for row in rows]) for i in range(len(rows[0]))]
            #    for i,row in enumerate(rows):
            #        print ' '.join([row[j].ljust(colwidths[j]) for j in range(len(colwidths))])
            #        if i == 0 or i == len(rows)-2:
            #            print '-'*(sum(colwidths)+len(colwidths)-1)
            #elif options.doinfo.startswith('joint'):
            #    env.Load(args[0],{'skipgeometry':'1'})
            #    body=env.GetBodies()[0]
            #    rows = [['name','joint_index','dof_index','parent_link','child_link','mimic']]
            #    for joint in body.GetJoints()+body.GetPassiveJoints():
            #        mimicnames=[]
            #        for idof in range(joint.GetDOF()):
            #            if joint.IsMimic(idof):
            #                mimicnames += [body.GetJointFromDOFIndex(idof2).GetName() for idof2 in joint.GetMimicDOFIndices(idof)]
            #        rows.append([joint.GetName(),str(joint.GetJointIndex()),str(joint.GetDOFIndex()),joint.GetHierarchyParentLink().GetName(),joint.GetHierarchyChildLink().GetName(),','.join(mimicnames)])
            #    rows.append(rows[0])
            #    colwidths = [max([len(row[i]) for row in rows]) for i in range(len(rows[0]))]
            #    for i,row in enumerate(rows):
            #        print ' '.join([row[j].ljust(colwidths[j]) for j in range(len(colwidths))])
            #        if i == 0 or i == len(rows)-2:
            #            print '-'*(sum(colwidths)+len(colwidths)-1)
            #else:
            #    sys.exit(1)

    finally:
        env.Destroy()
        

if __name__ == '__main__':
    res = parse_robot("../kawada-hironx.zae")
    for res_dict in res:
        for i in res_dict.keys():
            print(i, res_dict[i])
        print("="*20)
