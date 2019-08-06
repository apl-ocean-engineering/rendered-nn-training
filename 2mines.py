import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

def coordToImagespace(coord):
    x = (coord[0]+1)/2
    y = (((-1)*coord[2])+1)/2
    return LPoint2f(x,y)

mine1 = loader.loadModel("mine.egg")
mine1.reparentTo(render)
mine2 = loader.loadModel("mine.egg")
mine2.reparentTo(render)
light1 = Spotlight("slight")
light2 = Spotlight("slight")

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

def rerender(task):
    scene_id = random.randint(0,354)
    background = OnscreenImage(parent = render2d, image = "/home/caden/Pictures/backgrounds/bg_{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else
    
    proj_dummy = base.cam.attach_new_node("proj-dummy") # create a new node to hold the projected model
    line_node = GeomNode("lines")
    line_path = render2d.attach_new_node(line_node)
    proj_mat = camLens.get_projection_mat_inv() # read the lens' inverse projection matrix

    count = task.frame+6498
    labelFile = open("/home/caden/Pictures/mines2/labels/scene_{}.txt".format(count), "w+") # create the label file 

    mine1.setPos(random.uniform(-3.5,3.5),random.uniform(5,10),random.uniform(-2.5,2.5)) # set random position
    mine1.setHpr(random.uniform(-180,180),random.uniform(-180,180),random.uniform(-180,180)) # set random orientation
    mine2.setPos(random.uniform(-3.5,3.5),random.uniform(5,10),random.uniform(-2.5,2.5)) # set random position
    mine2.setHpr(random.uniform(-180,180),random.uniform(-180,180),random.uniform(-180,180)) # set random orientation

    proj_dummy.set_transform(TransformState.makeMat(proj_mat)) # set it as the matrix for the projected dummy
    min1, max1 = mine1.get_tight_bounds(proj_dummy) # get the bounding coordinates of the projection
    box1_LL, box1_UR = LPoint3f(min1[0],0,min1[1]), LPoint3f(max1[0],0,max1[1]) # coordinates in 2-space of the corners
    min2, max2 = mine2.get_tight_bounds(proj_dummy) # get the bounding coordinates of the projection
    box2_LL, box2_UR = LPoint3f(min2[0],0,min2[1]), LPoint3f(max2[0],0,max2[1]) # coordinates in 2-space of the corners

    box1_w = (max1[0] - min1[0])
    box1_h = (max1[1] - min1[1])
    center1 = LPoint3f(min1[0]+box1_w/2,0,min1[1]+(box1_h/2))
    box2_w = (max2[0] - min2[0])
    box2_h = (max2[1] - min2[1])
    center2 = LPoint3f(min2[0]+box2_w/2,0,min2[1]+(box2_h/2))

    '''segs = LineSegs()
    segs.move_to(box1_LL)
    segs.draw_to(min1[0], 0, max1[1])
    segs.draw_to(box1_UR)
    segs.draw_to(max1[0], 0, min1[1])
    segs.draw_to(box1_LL)

    line_node.remove_all_geoms()
    segs.create(line_node)'''

    light1.setColor((random.uniform(155,170)/255, random.uniform(175,185)/255, random.uniform(155,170)/255, 1)) # set light color and intensity
    spot1 = render.attachNewNode(light1)
    spot1.setPos(random.uniform(-10,10),random.uniform(-5,mine1.getPos()[1]),random.uniform(-10,10)) # set random position
    spot1.lookAt(mine1) # point it at the mine, wherever it is
    mine1.setLight(spot1) # assign the light to the mine
    light2.setColor((random.uniform(155,170)/255, random.uniform(175,185)/255, random.uniform(155,170)/255, 1)) # set light color and intensity
    spot2 = render.attachNewNode(light2)
    spot2.setPos(random.uniform(-10,10),random.uniform(-5,mine2.getPos()[1]),random.uniform(-10,10)) # set random position
    spot2.lookAt(mine2) # point it at the mine, wherever it is
    mine2.setLight(spot2) # assign the light to the mine

    print >>labelFile, str(0)+" "+str(coordToImagespace(center1).getX())+" "+str(coordToImagespace(center1).getY())+" "+str(box1_w/2)+" "+str(box1_h/2)
    print >>labelFile, str(0)+" "+str(coordToImagespace(center2).getX())+" "+str(coordToImagespace(center2).getY())+" "+str(box2_w/2)+" "+str(box2_h/2)
    
    image = PNMImage() # create PNMImage wrapper
    base.camNode.getDisplayRegion(0).getScreenshot(image) # grab a PNM screenshot of the display region
    imageFile = "/home/caden/Pictures/mines2/images/scene_{}.jpg".format(count-1) # set the filename (don't know why images and labels are 1 offset, but they are)
    image.write(Filename(imageFile)) # write the screenshot to the above file
    if (count-1)//10 == (count-1)/10.0: print("generated "+imageFile)
    labelFile.close()

    if count < 8000:
        return task.cont
    else:
        print "Render complete."
        return task.done

base.taskMgr.add(rerender, "render")
base.run()