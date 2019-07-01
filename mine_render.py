from math import *
from random import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

class mineRender(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        mine_x = uniform(-3,3)
        mine_y = uniform(5,10)
        mine_z = uniform(-2,2)
        mine_H = uniform(-180,180)
        mine_p = uniform(-180,180)
        mine_r = uniform(-180,180)
        light_x = uniform(-6,6)
        light_y = uniform(-6,6)
        light_z = uniform(-6,6)

        self.mine = self.loader.loadModel("models/mine") # load model
        self.mine.reparentTo(self.render) # add model to scene
        self.mine.setScale(1,1,1) # set model size
        self.mine.setPos(mine_x,mine_y,mine_z) # set random position
        self.mine.setHpr(mine_H,mine_p,mine_r) # set random orientation

        metalTex = loader.loadTexture('maps/bulkhead.jpg') # load model texture
        self.mine.setColor(44,55,37,0.5) # setTexture(metalTex)

        self.background = OnscreenImage(parent=render2d, image='maps/pool.jpg') # load background image
        base.cam2d.node().getDisplayRegion(0).setSort(-20) # make sure it renders behind everything else

        light = Spotlight('slight')
        light.setColor((1, 1, 1, 1)) # set light color and intensity
        self.spot = render.attachNewNode(light)
        self.spot.setPos(light_x,light_y,light_z) # set random position
        self.spot.lookAt(self.mine) # point it at the mine, wherever it is
        render.setLight(self.spot) # use the spot as the lighting for the rendered scene

        self.labelText = OnscreenText(text=("uptime: {}".format(0.0)+"\n{}".format(self.mine.getPos())+"\n{}".format(self.mine.getHpr())), # generate a text object for the label
            pos=(-0.75,-0.75), scale=0.07)

        self.taskMgr.add(self.updateText, "updateText") # add the text update function to the looping task tree

    def updateText(self, task):
        self.labelText.setText("uptime: {}".format(task.time)+"\n{}".format(self.mine.getPos())+"\n{}".format(self.mine.getHpr())) # refresh these values onscreen
        return Task.cont

mineRender().run()