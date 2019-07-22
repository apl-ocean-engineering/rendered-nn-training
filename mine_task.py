import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

camLens = base.cam.node().getLens()
camLens.setFocalLength(1833)
camLens.setFilmSize(2048, 1536)
#lens.setFilmOffset(w*0.5 - cx, h*0.5 - cy)
#lens.setNearFar(near, far)
#camLens.setAspectRatio()
M = camLens.getProjectionMat()
f = camLens.getFocalLength()
r = camLens.getAspectRatio()
w = int(camLens.getFilmSize()[0])
h = int(camLens.getFilmSize()[1])

props = WindowProperties() 
props.setSize(w, h) 
base.win.requestProperties(props)

mine = loader.loadModel("/home/caden/.local/lib/python2.7/site-packages/panda3d/models/mine.egg") # load model
mine.reparentTo(render) # add model to scene

light = Spotlight("slight") # create lighting container

def update_bg(task):
    scene_id = random.randint(0,354)
    background = OnscreenImage(parent = render2d, image = "/home/caden/Pictures/backgrounds/bg_{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-20) # make sure it renders behind everything else

    return task.cont

def reposition(task):
    mine_x = random.uniform(-3.5,3.5)
    mine_y = random.uniform(5,10)
    mine_z = random.uniform(-2.5,2.5)
    mine_H = random.uniform(-180,180)
    mine_p = random.uniform(-180,180)
    mine_r = random.uniform(-180,180)
    mine_scale = random.uniform(0.5,1.5)
    light_x = random.uniform(-10,10)
    light_y = random.uniform(-5,mine_y)
    light_z = random.uniform(-10,10)
    light_R = random.uniform(155,170)
    light_G = random.uniform(175,185)
    light_B = random.uniform(155,170)

    mine.setPos(mine_x,mine_y,mine_z) # set random position
    mine.setHpr(mine_H,mine_p,mine_r) # set random orientation
    mine.setScale(mine_scale) # set random size

    light.setColor((light_R/255, light_G/255, light_B/255, 1)) # set light color and intensity
    spot = render.attachNewNode(light)
    spot.setPos(light_x,light_y,light_z) # set random position
    spot.lookAt(mine) # point it at the mine, wherever it is
    mine.setLight(spot) # use the spot as the lighting for the rendered scene

    return task.cont

def project_write(task):
    proj_dummy = base.cam.attach_new_node("proj-dummy") # create a new node to hold the projected model
    line_node = GeomNode("lines")
    line_path = render2d.attach_new_node(line_node)
    
    proj_mat = camLens.get_projection_mat_inv() # read the lens' inverse projection matrix
    proj_dummy.set_transform(TransformState.makeMat(proj_mat)) # set it as the matrix for the projected dummy

    min, max = mine.get_tight_bounds(proj_dummy) # get the bounding coordinates in 2D

    box_w = (max[0] - min[0])/2
    box_h = (max[1] - min[1])/2
    xCenter, yCenter = ((min[0]+(0.5*box_w))+1.0)/2.0, ((-1)*(min[1]+(0.5*box_h))+1.0)/2.0
    
    segs = LineSegs()
    segs.move_to(min[0], 0, min[1])
    segs.draw_to(min[0], 0, max[1])
    segs.draw_to(max[0], 0, max[1])
    segs.draw_to(max[0], 0, min[1])
    segs.draw_to(min[0], 0, min[1])

    line_node.remove_all_geoms()
    #segs.create(line_node)

    count = task.frame

    base.camNode.getDisplayRegion(0).getScreenshot(PNMImage()) # grab a PNM screenshot of the display region
    imageFile = "/home/caden/Pictures/replacements/images/scene_{}.jpg".format(count) # set the filename
    PNMImage().write(Filename(imageFile)) # write the previously taken screenshot to the above file
    print("generated "+imageFile)
    labelFile = open("/home/caden/Pictures/replacements/labels/scene_{}.txt".format(count), "w+") # create the label file
    labelFile.write(str(0)+" "+str(xCenter)+" "+str(yCenter)+" "+str(box_w)+" "+str(box_h)) # write metadata to label file
    labelFile.close()
    
    if count < 100:
        return task.cont
    else:
        return task.done

base.taskMgr.add(update_bg, "background")
base.taskMgr.add(reposition, "reposition")
base.taskMgr.add(project_write, "project/write")

base.run()