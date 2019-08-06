import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

def coordToImagespace(coord):
    x = (coord[0]+1)/2
    y = (((-1)*coord[2])+1)/2
    return LPoint2f(x,y)

camLens = base.cam.node().getLens()
camLens.setFocalLength(1833)
camLens.setFilmSize(2048, 1536)
M = camLens.getProjectionMat()
f = camLens.getFocalLength()
r = camLens.getAspectRatio()
w = int(camLens.getFilmSize().getX())
h = int(camLens.getFilmSize().getY())

props = WindowProperties() 
props.setSize(w, h) 
base.win.requestProperties(props)

def rerender():
    scene_id = random.randint(0,354)
    #background = OnscreenImage(parent = render2d, image = "/home/caden/Pictures/backgrounds/bg_{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else
    
    mines = []
    lights = []
    spot = []
    metadata = []

    proj_dummy = base.cam.attach_new_node("proj-dummy") # create a new node to hold the projected model
    line_node = GeomNode("lines")
    line_path = render2d.attach_new_node(line_node)
    proj_mat = camLens.get_projection_mat_inv() # read the lens' inverse projection matrix

    count = 1
    labelFile = open("/home/caden/Pictures/mines2/labels/scene_{}.txt".format(count), "w+") # create the label file 
    num_mines = random.randint(1,3)

    for i in range(num_mines):
        mines.append(loader.loadModel("mine.egg"))
        mines[i].reparentTo(render)
        lights.append(Spotlight("slight"))

        mines[i].setPos(random.uniform(-3.5,3.5),random.uniform(5,10),random.uniform(-2.5,2.5)) # set random position
        mines[i].setHpr(random.uniform(-180,180),random.uniform(-180,180),random.uniform(-180,180)) # set random orientation

        lights[i].setColor((random.uniform(155,170)/255, random.uniform(175,185)/255, random.uniform(155,170)/255, 1)) # set light color and intensity
        spot.append(render.attachNewNode(lights[i]))
        spot[i].setPos(random.uniform(-10,10),random.uniform(-5,mines[i].getPos()[1]),random.uniform(-10,10)) # set random position
        spot[i].lookAt(mines[i]) # point it at the mine, wherever it is
        mines[i].setLight(spot[i]) # assign the light to the mine

        proj_dummy.set_transform(TransformState.makeMat(proj_mat)) # set it as the matrix for the projected dummy
        min, max = mines[i].get_tight_bounds(proj_dummy) # get the bounding coordinates of the projection
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

        segs.create(line_node)

        metadata.append(str(0)+" "+str(coordToImagespace(center).getX())+" "+str(coordToImagespace(center).getY())+" "+str(box_w/2)+" "+str(box_h/2)+"\n")
    print(str(num_mines)+" mine(s) and metadata added.")
    print("Getting screenshot...")
    image = PNMImage() # create PNMImage wrapper
    base.camNode.getDisplayRegion(0).getScreenshot(image) # grab a PNM screenshot of the display region
    imageFile = "/home/caden/Pictures/mines2/images/scene_{}.jpg".format(count-1) # set the filename (don't know why images and labels are 1 offset, but they are)
    image.write(Filename(imageFile)) # write the screenshot to the above file
    labelFile.writelines(metadata) # write the label data to separate lines
    print("generated image: "+imageFile+" and label file: /home/caden/Pictures/mines2/labels/scene_{}.txt".format(count))
    labelFile.close()

rerender()
base.run()