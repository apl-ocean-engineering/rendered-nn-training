import random, time, direct.directbase.DirectStart
from math import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import *

#background = OnscreenImage(parent = render) # load background image

mine = loader.loadModel("mine") # load model
mine.reparentTo(render) # add model to scene
mine.setScale(1,1,1) # set model size

metalTex = loader.loadTexture('maps/bulkhead.jpg') # load model texture
#mine.setTexture(metalTex)
mine.setColor(114,200,122,1)

light = Spotlight("slight")
light.setColor((1, 1, 1, 1)) # set light color and intensity
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
w = camLens.getFilmSize()[0]
h = camLens.getFilmSize()[1]

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

    # If project() returns false, it means the point was behind the lens.
    return None

for i in range(10):
    
    labelFile = open("/home/caden/Pictures/mines/labels/label_{}.txt".format(i), "w+")
    
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
    scaled_x = (projectedPos[0]+1)/2
    scaled_y = ((-1)*projectedPos[1]+1)/2

    scene_id = random.randint(0,381)
    background = OnscreenImage(parent = render2d, image = "maps/NBL_images/{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else

    spot.setPos(light_x,light_y,light_z) # set random position
    spot.lookAt(mine) # point it at the mine, wherever it is
    mine.setLight(spot) # use the spot as the lighting for the rendered scene

    #labelText = OnscreenText(text=(str(mine.getPos())),pos=(0.0,-0.9),scale=0.07) # generate a text object for the label
    #mine.showTightBounds() # draw 3D bounding box around model

    box = OnscreenImage(image = '/home/caden/Downloads/box.png', parent = mine, scale = (1.36,1,1.36))
    box.setTransparency(TransparencyAttrib.MAlpha)
    box.setBillboardPointEye()

    vertexList = list()
    normalList = list()
    projectedList = list()

    geomNodeCollection = mine.findAllMatches( '**/+GeomNode' ) # collect all geometry nodes
    for nodePath in geomNodeCollection: 
        geomNode = nodePath.node()
        for geom in range(geomNode.getNumGeoms()): # for each object in the render
            obj = geomNode.getGeom(geom)
            vData = obj.getVertexData() # pull the vertex data
            vReader = GeomVertexReader(vData, 'vertex') # read the vertex data

        while not vReader.isAtEnd(): # equivalent to: for i in range(len(list of vertices))
            vertex = vReader.getData3f()
            vertexList.append(vertex)

    for point in vertexList:
        projectedPoint = compute2dPosition(mine, point)
        if projectedPoint != None:
            projectedList.append(projectedPoint)

    xmax = max(projectedList, key=lambda item: item[0])[0]
    ymax = max(projectedList, key=lambda item: item[1])[1]
    xmin = min(projectedList, key=lambda item: item[0])[0]
    ymin = min(projectedList, key=lambda item: item[1])[1]

    line_node = GeomNode("lines")
    line_path = render2d.attach_new_node(line_node)

    segs = LineSegs()
    segs.move_to(xmin, 0, ymin)
    segs.draw_to(xmax, 0, ymin)
    segs.draw_to(xmax, 0, ymax)
    segs.draw_to(xmin, 0, ymax)
    segs.draw_to(xmin, 0, ymin)

    box_w = xmax-xmin
    box_h = ymax-ymin

    line_node.remove_all_geoms()
    segs.create(line_node)

    path = "/home/caden/Pictures/mines/images/scene_{}.jpg".format(i)
    renderToPNM().write(Filename(path))
    print("generated "+path)
    labelFile.write(str([0, scaled_x, scaled_y, box_w, box_h]))
    labelFile.close()

#base.run()