import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

background = OnscreenImage(parent = render) # load background image

mine = loader.loadModel("mine") # load model
mine.reparentTo(render) # add model to scene
mine.setScale(1,1,1) # set model size

metalTex = loader.loadTexture('maps/bulkhead.jpg') # load model texture
mine.setTexture(metalTex)

light = Spotlight("slight")
light.setColor((1, 1, 1, 1)) # set light color and intensity
spot = render.attachNewNode(light)

#K = [[f, s, cx], [0, a, cy], [0, 0, 1]]
#camLens = MatrixLens.setUserMat(K)
camera.getChild(0).node().getLens().setFocalLength(1000)
camera.getChild(0).node().getLens().setFilmSize(1920, 1080)
#lens.setFilmOffset(w*0.5 - cx, h*0.5 - cy)
#lens.setNearFar(near, far)
#camera.getChild(0).node().getLens().setAspectRatio(1)
matrix = camera.getChild(0).node().getLens().getProjectionMat()
print matrix 


def renderToPNM():
    base.graphicsEngine.renderFrame() # Render the frame

    image = PNMImage() # init variable to store the image (PNMImage is an image manipulation class native to Panda3D)
    dr = base.camNode.getDisplayRegion(0) # set display region to the default
    dr.getScreenshot(image) # Store the rendered frame into the variable screenshot

    return image

for i in range(1):
    mine_x = random.uniform(-3,3)
    mine_y = 2 #random.uniform(5,15)
    mine_z = random.uniform(-2,2)
    mine_H = random.uniform(-180,180)
    mine_p = random.uniform(-180,180)
    mine_r = random.uniform(-180,180)
    light_x = random.uniform(-10,10)
    light_y = random.uniform(-5,mine_y)
    light_z = random.uniform(-10,10)

    mine.setPos(mine_x,mine_y,mine_z) # set random position
    mine.setHpr(mine_H,mine_p,mine_r) # set random orientation

    scene_id = random.randint(0,432)
    background = OnscreenImage(parent = render2d, image = "maps/NBL_images/{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else

    spot.setPos(light_x,light_y,light_z) # set random position
    spot.lookAt(mine) # point it at the mine, wherever it is
    render.setLight(spot) # use the spot as the lighting for the rendered scene

    labelText = OnscreenText(text=(str(mine.getTightBounds())),pos=(0.0,-1),scale=0.07) # generate a text object for the label
    mine.showTightBounds() # draw 3D bounding box around model

    path = "/home/caden/Pictures/renders/scene_{}.jpg".format(i)
    #renderToPNM().write(Filename(path))
    #print("generated "+path)
    
    
    P = camera.getChild(0).node().getLens().getProjectionMat()
    f = camera.getChild(0).node().getLens().getFocalLength()
    r = camera.getChild(0).node().getLens().getAspectRatio()
    

    geomNodeCollection = mine.findAllMatches('**/+GeomNode')
    for nodePath in geomNodeCollection:
        geomNode = nodePath.node()
        for i in range(geomNode.getNumGeoms()):
            geom = geomNode.getGeom(i)
            state = geomNode.getGeomState(i)
            #print geom
            #print state

base.run()