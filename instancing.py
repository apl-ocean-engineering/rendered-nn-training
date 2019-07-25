import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

def renderToPNM():
    base.graphicsEngine.renderFrame() # Render the frame

    image = PNMImage() # init variable to store the image (PNMImage is an image manipulation class native to Panda3D)
    dr = base.camNode.getDisplayRegion(0) # set display region to the default
    dr.getScreenshot(image) # grab a screenshot of the DR and write it to the image

    return image

mine = loader.loadModel("mine.egg") 
mineParent = render.attachNewNode('mineParent')

light = Spotlight("slight")

camLens = base.cam.node().getLens()
camLens.setFocalLength(1833)
camLens.setFilmSize(2048, 1536)
M = camLens.getProjectionMat()
f = camLens.getFocalLength()
r = camLens.getAspectRatio()
w = int(camLens.getFilmSize()[0])
h = int(camLens.getFilmSize()[1])

props = WindowProperties() 
props.setSize(w, h) 
base.win.requestProperties(props)

def coordToImagespace(coord):
    x = (coord[0]+1)/2
    y = 0
    z = (((-1)*coord[2])+1)/2
    return LPoint3f(x,y,z)

for i in range(5):
    scene_id = random.randint(0,354)
    #background = OnscreenImage(parent = render2d, image = "/home/caden/Pictures/backgrounds/bg_{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else
    
    proj_dummy = base.cam.attach_new_node("proj-dummy") # create a new node to hold the projected model
    line_node = GeomNode("lines")
    line_path = render2d.attach_new_node(line_node)
    proj_mat = camLens.get_projection_mat_inv() # read the lens' inverse projection matrix

    num_mines = 3#int(random.triangular(1,3,1))
    labelFile = open("/home/caden/Pictures/mines2/labels/scene_{}.txt".format(i), "w+") # create the label file 

    for n in range(num_mines):
        minePlacer = mineParent.attachNewNode("minePlacer")
        mineInstance = mine.instanceTo(minePlacer)
        minePlacer.setPos(random.uniform(-3.5,3.5),random.uniform(5,10),random.uniform(-2.5,2.5)) # set random position
        minePlacer.setHpr(random.uniform(-180,180),random.uniform(-180,180),random.uniform(-180,180)) # set random orientation

        proj_dummy.set_transform(TransformState.makeMat(proj_mat)) # set it as the matrix for the projected dummy
        min, max = minePlacer.get_tight_bounds(proj_dummy) # get the bounding coordinates of the projection
        box_LL, box_UR = LPoint3f(min[0],0,min[1]), LPoint3f(max[0],0,max[1]) # coordinates in 2-space of the corners
        diagonal = LVector3f(box_UR - box_LL)

        box_w = (max[0] - min[0])
        box_h = (max[1] - min[1])
        center = LPoint3f(min[0]+box_w/2,0,min[1]+(box_h/2))

        segs = LineSegs()
        segs.move_to(box_LL)
        segs.draw_to(min[0], 0, max[1])
        segs.draw_to(box_UR)
        segs.draw_to(max[0], 0, min[1])
        segs.draw_to(box_LL)

        #line_node.remove_all_geoms()
        segs.create(line_node)
        
        light.setColor((random.uniform(155,170)/255, random.uniform(175,185)/255, random.uniform(155,170)/255, 1)) # set light color and intensity
        spot = render.attachNewNode(light)
        spot.setPos(random.uniform(-10,10),random.uniform(-5,minePlacer.getPos()[1]),random.uniform(-10,10)) # set random position
        spot.lookAt(minePlacer) # point it at the mine, wherever it is
        minePlacer.setLight(spot) # assign the light to the mine

        print >>labelFile, str(0)+" "+str(coordToImagespace(center)[0])+" "+str(coordToImagespace(center)[2])+" "+str(box_w/2)+" "+str(box_h/2)

    image = PNMImage() # create PNMImage wrapper
    base.camNode.getDisplayRegion(0).getScreenshot(image) # grab a PNM screenshot of the display region
    imageFile = "/home/caden/Pictures/mines2/images/scene_{}.jpg".format(i) # set the filename (don't know why images and labels are 1 offset, but they are)
    image.write(Filename(imageFile)) # write the screenshot to the above file
    #labelFile.write(str(0)+" "+str(coordToImagespace(center)[0])+" "+str(coordToImagespace(center)[2])+" "+str(box_w/2)+" "+str(box_h/2)+"\n")
    labelFile.close()

base.run()