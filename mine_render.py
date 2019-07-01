import random
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *
import direct.directbase.DirectStart


mine_x = random.uniform(-3,3)
mine_y = random.uniform(5,15)
mine_z = random.uniform(-2,2)
mine_H = random.uniform(-180,180)
mine_p = random.uniform(-180,180)
mine_r = random.uniform(-180,180)
light_x = random.uniform(-10,10)
light_y = random.uniform(-5,mine_y)
light_z = random.uniform(-10,10)

mine = loader.loadModel("models/mine") # load model
mine.reparentTo(render) # add model to scene
mine.setScale(1,1,1) # set model size
mine.setPos(mine_x,mine_y,mine_z) # set random position
mine.setHpr(mine_H,mine_p,mine_r) # set random orientation

metalTex = loader.loadTexture('maps/bulkhead.jpg') # load model texture
mine.setColor(88,110,74,1) # setTexture(metalTex)

background = OnscreenImage(parent=render2d, image='maps/pool.jpg') # load background image
base.cam2d.node().getDisplayRegion(0).setSort(-20) # make sure it renders behind everything else

light = Spotlight('slight')
light.setColor((1, 1, 1, 1)) # set light color and intensity
spot = render.attachNewNode(light)
spot.setPos(light_x,light_y,light_z) # set random position
spot.lookAt(mine) # point it at the mine, wherever it is
render.setLight(spot) # use the spot as the lighting for the rendered scene

labelText = OnscreenText(text=("light: {}".format(spot.getPos())+"\n{}".format(mine.getPos())+"\n{}".format(mine.getHpr())), # generate a text object for the label
    pos=(-0.75,-0.75), scale=0.07)

base.run()