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
mine.setTexture(metalTex)
mine.setColorScale(114,200,122,1)

light = Spotlight("slight")
light.setColor((1, 1, 1, 0.01)) # set light color and intensity
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
print M

def renderToPNM():
    base.graphicsEngine.renderFrame() # Render the frame

    image = PNMImage() # init variable to store the image (PNMImage is an image manipulation class native to Panda3D)
    dr = base.camNode.getDisplayRegion(0) # set display region to the default
    dr.getScreenshot(image) # grab a screenshot of the DR and write it to the image

    return image

def compute2dPosition(nodePath, point = Point3(0, 0, 0)):
    """ Computes a 3-d point, relative to the indicated node, into a
    2-d point as seen by the camera.  The range of the returned value
    is based on the len's current film size and film offset, which is
    (-1 .. 1) by default. """
    
    # Convert the point into the camera's coordinate space
    p3d = base.cam.getRelativePoint(nodePath, point)

    # Ask the lens to project the 3-d point to 2-d.
    p2d = Point2()
    if base.camLens.project(p3d, p2d):
        # Got it!
        return p2d

    # If project() returns false, it means the point was behind the
    # lens.
    return None

for i in range(1):
    
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

    x_pos = (mine.getPos()[0]*f/mine.getPos()[1]) + 1
    y_pos = (mine.getPos()[2]*(-f)/mine.getPos()[1]) + 1

    scene_id = random.randint(0,381)
    background = OnscreenImage(parent = render2d, image = "maps/NBL_images/{}.png".format(scene_id)) # load background image
    base.cam2d.node().getDisplayRegion(0).setSort(-1) # make sure it renders behind everything else

    spot.setPos(light_x,light_y,light_z) # set random position
    spot.lookAt(mine) # point it at the mine, wherever it is
    mine.setLight(spot) # use the spot as the lighting for the rendered scene

    #labelText = OnscreenText(text=(str(mine.getPos())),pos=(0.0,-0.9),scale=0.07) # generate a text object for the label
    #mine.showTightBounds() # draw 3D bounding box around model

    box = OnscreenImage(image = '/home/caden/Downloads/box.png', parent = mine, scale = (1.35,1,1.35))
    box.setTransparency(TransparencyAttrib.MAlpha)
    box.setBillboardPointEye()

    path = "/home/caden/Pictures/mines/images/scene_{}.jpg".format(i)
    renderToPNM().write(Filename(path))
    print("generated "+path)
    labelFile.write(str([0, x_pos/w, y_pos/h]))
    labelFile.close()

'''geomNodeCollection = mine.findAllMatches('**/+GeomNode')
for nodePath in geomNodeCollection:
    geomNode = nodePath.node()
    for vertex in range(geomNode.getNumGeoms()):
        geom = geomNode.getGeom(vertex)
        state = geomNode.getGeomState(vertex)
    print geom
    #print state'''

geomNodeCollection = mine.findAllMatches( '**/+GeomNode' )
geomNodePath = geomNodeCollection[0]
geomNode = geomNodePath.node()
geom = geomNode.getGeom(0)
vData = geom.getVertexData()
reader_vertex = GeomVertexReader( vData, 'vertex' )
reader_normal = GeomVertexReader( vData, 'normal' )

vertexList = list()
normalList = list()

for i in xrange( 2000 ) :

    vertex = reader_vertex.getData3f()
    normal = reader_normal.getData3f()

    vertexList.append( vertex )
    normalList.append( normal )

projectedList = list()

for point in vertexList:
    projectedPoint = compute2dPosition(mine, point)
    if projectedPoint != None:
        projectedList.append(projectedPoint)

print projectedList

#base.run()