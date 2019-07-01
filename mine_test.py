from math import pi, sin, cos, tan
from random import randint
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

class mineRender(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.mine = self.loader.loadModel("models/mine")
        self.mine.reparentTo(self.render)
        self.mine.setScale(1,1,1)
        self.mine.setPos(0,0,0)
            
        metalTex = loader.loadTexture('maps/bulkhead.jpg')
        self.mine.setColor(44,55,37,1) # setTexture(metalTex)

        self.background = OnscreenImage(parent=render2d, image='maps/pool.jpg')
        base.cam2d.node().getDisplayRegion(0).setSort(-20) 

        light = Spotlight('slight')
        light.setColor((1, 1, 1, 1))
        self.spot = render.attachNewNode(light)
        self.spot.setPos(6,6,6)
        self.spot.lookAt(self.mine)
        render.setLight(self.spot)

        self.labelText = OnscreenText(text=("runtime: {}".format(0)+"\ncamera_pos: {}".format(self.camera.getPos())+"\ncamera_Hpr: {}".format(self.camera.getHpr())), 
            pos=(-0.6,-0.8), scale=0.07)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
        self.taskMgr.add(self.spinLightTask, "SpinLightTask")
        self.taskMgr.add(self.updateText, "updateText")

    def updateText(self, task):
        self.labelText.setText("runtime: {}".format(task.time)+"\ncamera_pos: {}".format(self.camera.getPos())+"\ncamera_Hpr: {}".format(self.camera.getHpr()))
        return Task.cont
    
    def spinCameraTask(self, task):
        angleDegrees = task.time * 10.0
        angleRadians = angleDegrees * (pi/180.0)
        self.camera.setPos(8*sin(angleRadians),-8*cos(angleRadians),4)
        #self.camera.setHpr(angleDegrees,0,0)
        self.camera.lookAt(self.mine)
        return Task.cont

    def spinLightTask(self, task):
        angleDegrees = task.time * 10.0
        angleRadians = angleDegrees * (pi/180.0)
        self.spot.setPos(20*sin(angleRadians-2),-20*cos(angleRadians-2),10)
        #self.spot.setHpr(angleDegrees,0,0)
        self.spot.lookAt(self.mine)
        return Task.cont

mineRender().run()