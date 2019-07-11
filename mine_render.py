import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

mine = loader.loadModel("/home/caden/.local/lib/python2.7/site-packages/panda3d/models/mine.egg") # load model
mine.reparentTo(render) # add model to scene
mine.setScale(1,1,1) # set model size

metalTex = loader.loadTexture('/home/caden/.local/lib/python2.7/site-packages/panda3d/models/maps/bulkhead.jpg') # load model texture
#mine.setTexture(metalTex)
mine.setColor(114,200,122,1)

light = Spotlight("slight")
light.setColor((1.51/2.0, 1.60/2.0, 1.59/2.0, 1)) # set light color and intensity
spot = render.attachNewNode(light)

camLens = camera.getChild(0).node().getLens()
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

def renderToPNM():
    base.graphicsEngine.renderFrame() # Render the frame

    image = PNMImage() # init variable to store the image (PNMImage is an image manipulation class native to Panda3D)
    dr = base.camNode.getDisplayRegion(0) # set display region to the default
    dr.getScreenshot(image) # grab a screenshot of the DR and write it to the image

    return image

def compute2dPosition(nodePath, point):
    # Convert the point into the camera's coordinate space
    p3d = base.cam.getRelativePoint(nodePath, point)

    # Ask the lens to project the 3-d point to 2-d.
    p2d = Point2()
    if base.camLens.project(p3d, p2d):
        # Got it!
        return p2d

    # returning False signifies that the point was outside the FOV
    return None

for i in range(1):
    props = WindowProperties() 
    props.setSize(w, h) 
    base.win.requestProperties(props) 

    mine_x = random.uniform(-3,3)
    mine_y = random.uniform(5,10)
    mine_z = random.uniform(-2,2)
    mine_H = random.uniform(-180,180)
    mine_p = random.uniform(-180,180)
    mine_r = random.uniform(-180,180)
    light_x = random.uniform(-10,10)
    light_y = random.uniform(-5,mine_y)
    light_z = random.uniform(-10,10)

    mine.setPos(mine_x,mine_y,mine_z) # set random position
    mine.setHpr(mine_H,mine_p,mine_r) # set random orientation
    projectedPos = compute2dPosition(mine, (0,0,0))
    xCenter = (projectedPos[0]+1.0)/2.0
    yCenter = ((-1.0)*projectedPos[1]+1.0)/2.0

    scene_id = random.randint(0,381)
    background = OnscreenImage(parent = render2d, image = "/home/caden/.local/lib/python2.7/site-packages/panda3d/models/maps/NBL_images/{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else

    spot.setPos(light_x,light_y,light_z) # set random position
    spot.lookAt(mine) # point it at the mine, wherever it is
    mine.setLight(spot) # use the spot as the lighting for the rendered scene

    proj_dummy = base.cam.attach_new_node("proj-dummy")
    line_node = GeomNode("lines")
    line_path = render2d.attach_new_node(line_node)
    
    proj_mat = base.cam.node().get_lens().get_projection_mat_inv()
    proj_dummy.set_transform(TransformState.makeMat(proj_mat))

    min, max = mine.get_tight_bounds(proj_dummy)
    
    box_w = (max[0] - min[0])/2
    box_h = (max[1] - min[1])/2
    box_center = LPoint2f(((min[0]+(0.5*box_w))+1.0)/2.0,((-1)*(min[1]+(0.5*box_h))+1.0)/2.0)

    segs = LineSegs()
    segs.move_to(min[0], 0, min[1])
    segs.draw_to(min[0], 0, max[1])
    segs.draw_to(max[0], 0, max[1])
    segs.draw_to(max[0], 0, min[1])
    segs.draw_to(min[0], 0, min[1])

    line_node.remove_all_geoms()
    segs.create(line_node)

    path = "/home/caden/Pictures/mines/images/scene_{}.jpg".format(i)
    renderToPNM().write(Filename(path))
    print("generated "+path)
    labelFile = open("/home/caden/Pictures/mines/labels/scene_{}.txt".format(i), "w+")
    labelFile.write(str(0)+" "+str(xCenter)+" "+str(yCenter)+" "+str(box_w)+" "+str(box_h))
    labelFile.close()

#base.run()