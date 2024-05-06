#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# This is an EXUDYN python utility library
#
# Details:  Utility functions for visualization, which provides functions for basic shapes
#           like cube, cylinder, sphere, solid of revolution. Functions generate dictionaries
#           which contain line, text or triangle primitives for drawing in Exudyn using OpenGL.
#
# Author:   Johannes Gerstmayr
# Date:     2020-07-26 (created)
#
# Copyright:This file is part of Exudyn. Exudyn is free software. You can redistribute it and/or modify it under the terms of the Exudyn license. See 'LICENSE.txt' for more details.
#
# Notes:    Some useful colors are defined, using RGBA (Red, Green, Blue and Alpha = opacity) channels
#           in the range [0,1], e.g., red = [1,0,0,1].\\
#           Available colors are: color4red, color4green, color4blue, color4cyan, color4magenta, color4yellow, color4orange, color4pink, color4lawngreen, color4violet, color4springgreen, color4dodgerblue, color4grey, color4darkgrey, color4lightgrey, color4lightred, color4lightgreen, color4steelblue, color4brown, color4black, color4darkgrey2, color4lightgrey2, color4white\\
#           Additionally, a list of 16 colors 'color4list' is available, which is intended to be used, e.g., for creating n bodies with different colors
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

import exudyn.basicUtilities as ebu
from exudyn.rigidBodyUtilities import ComputeOrthonormalBasisVectors, HomogeneousTransformation, \
                                      HT2rotationMatrix, HT2translation

#constants and fixed structures:
import numpy as np #LoadSolutionFile
import copy as copy #to be able to copy e.g. lists
from math import pi, sin, cos
#import time        #AnimateSolution

# color definitions
color4red = [1.,0.,0.,1.]
color4green = [0.,1.,0.,1.]
color4blue = [0.,0.,1.,1.]

color4cyan = [0.,1.,1.,1.]
color4magenta = [1.,0.,1.,1.]
color4yellow = [1.,1.,0.,1.]

color4orange = [1.,0.5,0.,1.]
color4pink = [1.,0.,0.5,1.]
color4lawngreen = [0.5,1.,0.,1.]

color4springgreen = [0.,1.,0.5,1.]
color4violet = [0.5,0.,1.,1.]
color4dodgerblue = [0.,0.5,1.,1.]


color4lightred = [0.9,0.4,0.4,1.]
color4lightgreen = [0.4,0.9,0.4,1.]
color4steelblue = [0.4,0.4,0.9,1.]
color4brown = [0.65,0.2,0.2,1.]

color4black =      [0.,0.,0.,1.]
color4darkgrey =   [0.2,0.2,0.2,1.]
color4darkgrey2 =  [0.35,0.35,0.35,1.]
color4grey =       [0.5,0.5,0.5,1.]
color4lightgrey =  [0.7,0.7,0.7,1.]
color4lightgrey2 = [0.85,0.85,0.85,1.]
color4white =      [1.,1.,1.,1.]

color4default =    [-1.,-1.,-1.,-1.] #indicates that default color is used

#define a list of 16 colors for numbered colors
color4list = [color4red, color4green, color4blue, 
              color4cyan, color4magenta, color4yellow,
              color4orange, color4pink, color4lawngreen,
              color4violet, color4springgreen, color4dodgerblue,
              color4grey, color4darkgrey, color4lightgrey,
              #color4lightred, color4lightgreen, color4steelblue, 
              color4brown]

color4listSize = len(color4list) #maximum number of colors in color4list

normalsFactor = 1. #this is a factor being either -1. [original normals pointing inside; until 2022-06-27], while +1. gives corrected normals pointing outside
switchTriangleOrder = False #this is the old ordering of triangles in some Sphere or Cylinder functions, causing computed normals to point inside

#**function: helper function to switch order of three items in a list; mostly used for reverting normals in triangles
#**input: 3D vector as list or as np.array
#**output: interchanged 2nd and 3rd component of list
def SwitchTripletOrder(vector):
    v=list(vector) #copy, such that vector is not changed
    a = v[2]
    v[2] = v[1]
    v[1] = a
    return v

#**function: compute normalized normal for 3 triangle points
#**input: 3D vector as list or as np.array
#**output: normal as np.array
def ComputeTriangleNormal(p0,p1,p2):
    v0 = np.array(p1) - np.array(p0)
    v1 = np.array(p2) - np.array(p0)
    # print(v0,v1)
    n = np.cross(v0,v1)
    ln = np.linalg.norm(n)
    if ln != 0.:
        n /= ln
    return n

#**function: compute area of triangle given by 3 points
#**input: 3D vector as list or as np.array
#**output: area as float
def ComputeTriangleArea(p0,p1,p2):
    return 0.5*np.linalg.norm(np.cross(np.array(p1) - np.array(p0), np.array(p2) - np.array(p0)))

#************************************************
#**function: convert graphics data into list of points and list of triangle indices (triplets)
#**input: g contains a GraphicsData with type TriangleList
#**output: returns [points, triangles], with points as list of np.array with 3 floats per point and triangles as a list of np.array with 3 int per triangle (0-based indices to points)
def GraphicsData2PointsAndTrigs(g):
    if g['type'] == 'TriangleList':
        nPoints=int(len(g['points'])/3)
        points = [np.zeros(3)]*nPoints
        for i in range(nPoints):
            points[i] = np.array(g['points'][i*3:i*3+3])
        
        nTrigs=int(len(g['triangles'])/3)
        triangles = [np.zeros(3, dtype=int)]*nTrigs
        for i in range(nTrigs):
            triangles[i] = np.array(g['triangles'][i*3:i*3+3], dtype=int)
    else:
        raise ValueError ('ERROR: GraphicsData2TrigsAndPoints(...) only takes GraphicsData of type TriangleList but found: '+
                          g['type'] )

    return [points, triangles]

#**function: convert triangles and points as returned from GraphicsData2TrigsAndPoints(...) 
#**input: 
#  points: list of np.array with 3 floats per point 
#  triangles: list of np.array with 3 int per triangle (0-based indices to triangles)
#  color: provided as list of 4 RGBA values or single list of (number of points)*[4 RGBA values]
#**output: returns GraphicsData with type TriangleList
def GraphicsDataFromPointsAndTrigs(points, triangles, color=[0.,0.,0.,1.]):
    pointList = list(np.array(points).flatten())
    triangleList = list(np.array(triangles).flatten())
    nPoints = int(len(pointList)/3)
    if len(color) == 4*nPoints:
        colorList = list(color) #without list() potential problem with mutable default value
    elif len(color) == 4:
        colorList = list(color)*nPoints
    else:
        print('number of points=', nPoints)
        print('number of trigs=', len(triangleList)/3)
        print('number of colors=', len(color))
        raise ValueError('GraphicsDataFromPointsAndTrigs: color must have either 4 RGBA values or 4*(number of points) RGBA values as a list')
    data = {'type':'TriangleList', 
            'colors': colorList, 
            'points':pointList, 
            'triangles':triangleList}
    return data

#************************************************
#**function: refine triangle mesh; every triangle is subdivided into 4 triangles
#**input:
#  points: list of np.array with 3 floats per point 
#  triangles: list of np.array with 3 int per triangle (0-based indices to triangles)
#**output: returns [points2, triangles2] containing the refined mesh; if the original mesh is consistent, no points are duplicated; if the mesh is not consistent, some mesh points are duplicated!
#**notes: becomes slow for meshes with more than 5000 points
def RefineMesh(points, triangles):
    # 2
    # |\
    # a c
    # |  \
    # 0-b-1
    points2 = copy.deepcopy(points)
    triangles2 = []
    
    #build point2trig list for efficiency, at most, per triangle 3 new points:
    trigsPerPoint = [ [] for _ in range(len(points) + len(triangles)*3) ]
    # for (ti, trig) in enumerate(triangles):
    #     for i in trig:
    #         trigsPerPoint[i] += [ti]

    #print(trigsPerPoint)
    pnew = [0,0,0] #a,b,c
    for (ti, trig) in enumerate(triangles):
        # print('process trig', ti)
        for j in range(3):
            pointNew = 0.5*(np.array(points[trig[j]])+np.array(points[trig[j-1]]))
            found = -1
            #search all points (SLOW):
            # for (i, p) in enumerate(points2):
            #     if np.linalg.norm(pointNew-p) <= 1e-12:
            #         found = i
            #go through all triangles at one point, if new (refined) trig exists, it contains the new point:
            for (i, ti2) in enumerate(trigsPerPoint[trig[j]]):
                # print('  i, ti2=', i, ti2)
                for pointIndex in triangles2[ti2]:
                    if np.linalg.norm(pointNew-points2[pointIndex]) <= 1e-12:
                        found = pointIndex

            if found==-1:
                pnew[j] = len(points2)
                # print('add new point ', pnew[j])
                points2 += [pointNew]
            else:
                pnew[j] = found
        toff = len(triangles2)
        triangles2 += [np.array([trig[0],pnew[1],pnew[0]],dtype=int)]
        triangles2 += [np.array([trig[1],pnew[2],pnew[1]],dtype=int)]
        triangles2 += [np.array([trig[2],pnew[0],pnew[2]],dtype=int)]
        triangles2 += [np.array([pnew[0],pnew[1],pnew[2]],dtype=int)]
        #add new triangles to trigsPerPoint:
        for (ti, trig) in enumerate(triangles2[-4:]):
            for i in trig:
                trigsPerPoint[i] += [toff+ti]
    # print('trigs per point=',trigsPerPoint)
    return [points2, triangles2]

#************************************************
#**function: shrink mesh using triangle normals; every point is at least moved a distance 'distance' normal from boundary
#**input:
#  points: list of np.array with 3 floats per point 
#  triangles: list of np.array with 3 int per triangle (0-based indices to triangles)
#  distance: float value of minimum distance
#**output: returns [points2, triangles2] containing the refined mesh; currently the points of the subdivided triangles are duplicated!
#**notes: ONLY works for consistent meshes (no duplicated points!)
def ShrinkMeshNormalToSurface(points, triangles, distance):
    points2 = copy.deepcopy(points)
    triangles2 = copy.deepcopy(triangles)
    #disp = [np.zeros(3).copy()]*len(points2) #copy, otherwise linked!!!
    disp = copy.deepcopy(points)
    for i in range(len(points2)):
        disp[i] *= 0.
    
    for trig in triangles:
        n = ComputeTriangleNormal(points[trig[0]],points[trig[1]],points[trig[2]])
        # print(n)
        for i in range(3):
            dn = -distance*n
            # print('move',trig[i],'=',dn, ', disp=',disp[trig[i]])
            for j in range(3):
                if abs(dn[j]) > abs(disp[trig[i]][j]):
                    disp[trig[i]][j] = dn[j]
                    # print('==>disp',trig[i],'=',disp[trig[i]])

    # print('disp=', disp)

    for i in range(len(points2)):
        points2[i] += disp[i]

    return [points2, triangles2]


#************************************************
#**function: add rigid body transformation to GraphicsData, using position offset (global) pOff (list or np.array) and rotation Aoff (transforms local to global coordinates; list of lists or np.array); see Aoff how to scale coordinates!
#**input:
#  g: graphicsData to be transformed
#  pOff: 3D offset as list or numpy.array added to rotated points
#  Aoff: 3D rotation matrix as list of lists or numpy.array with shape (3,3); if A is scaled by factor, e.g. using 0.001*np.eye(3), you can also scale the coordinates!!!
#**output: returns new graphcsData object to be used for drawing in objects
#**notes: transformation corresponds to HomogeneousTransformation(Aoff, pOff), transforming original coordinates v into vNew = pOff + Aoff @ v
def MoveGraphicsData(g, pOff, Aoff):
    p0 = np.array(pOff)
    A0 = np.array(Aoff)
    
    if g['type'] == 'TriangleList': 
        gNew = {'type':'TriangleList'}
        gNew['colors'] = copy.copy(g['colors'])
        gNew['triangles'] = copy.copy(g['triangles'])
        if 'edges' in g:
            gNew['edges'] = copy.copy(g['edges'])
        if 'edgeColor' in g:
            gNew['edgeColor'] = copy.copy(g['edgeColor'])

        n=int(len(g['points'])/3)
        v0 = np.array(g['points'])
        v = np.kron(np.ones(n),p0) + (A0 @ v0.reshape((n,3)).T).T.flatten()
        
        gNew['points'] = list(v)
        if 'normals' in g:
            n0 = np.array(g['normals'])
            gNew['normals'] = list((A0 @ n0.reshape((n,3)).T).T.flatten() )
        
        # #original, slow:
        # for i in range(n):
        #     v = gNew['points'][i*3:i*3+3]
        #     v = p0 + A0 @ v
        #     gNew['points'][i*3:i*3+3] = list(v)
        # if 'normals' in gNew:
        #     n=int(len(g['normals'])/3)
        #     for i in range(n):
        #         v = gNew['normals'][i*3:i*3+3]
        #         v = A0 @ v
        #         gNew['normals'][i*3:i*3+3] = list(v)
    elif g['type'] == 'Line':
        gNew = copy.deepcopy(g)
        n=int(len(g['data'])/3)
        for i in range(n):
            v = gNew['data'][i*3:i*3+3]
            v = p0 + A0 @ v
            gNew['data'][i*3:i*3+3] = list(v)
    elif g['type'] == 'Text':
        gNew = copy.deepcopy(g)
        v = p0 + A0 @ gNew['position']
        gNew['position'] = list(v)
    elif g['type'] == 'Circle':
        gNew = copy.deepcopy(g)
        v = p0 + A0 @ gNew['position']
        gNew['position'] = list(v)
        if 'normal' in gNew:
            v = A0 @ gNew['normal']
            gNew['normal'] = list(v)
    else:
        raise ValueError('MoveGraphicsData: unsupported graphics data type')
    return gNew

#************************************************
#**function: merge 2 different graphics data with triangle lists
#**input: graphicsData dictionaries g1 and g2 obtained from GraphicsData functions
#**output: one graphicsData dictionary with single triangle lists and compatible points and normals, to be used in visualization of EXUDYN objects; edges are merged; edgeColor is taken from graphicsData g1
def MergeGraphicsDataTriangleList(g1,g2):
    np = int(len(g1['points'])/3) #number of points
    useNormals = False
    if 'normals' in g1 and 'normals' in g2:
        useNormals = True

    if np*4 != len(g1['colors']):
        raise ValueError('MergeGraphicsDataTriangleList: incompatible colors and points in lists')

    if useNormals:
        if np*3 != len(g1['normals']):
            raise ValueError('MergeGraphicsDataTriangleList: incompatible normals and points in lists')
        data = {'type':'TriangleList', 'colors':copy.copy(g1['colors']), 'normals':copy.copy(g1['normals']), 
                'points': copy.copy(g1['points']), 'triangles': copy.copy(g1['triangles'])}

        data['normals'] += g2['normals']
    else:
        data = {'type':'TriangleList', 'colors':copy.copy(g1['colors']),
                'points': copy.copy(g1['points']), 'triangles': copy.copy(g1['triangles'])}
    
    data['colors'] += g2['colors']
    data['points'] += g2['points']

    #copy and merge edges; edges can be available only in one triangle list
    if 'edges' in g1:
        data['edges'] = copy.copy(g1['edges'])
    if 'edges' in g2:
        edges2 = copy.copy(g2['edges'])
        if 'edges' not in data:
            data['edges'] = []
        else:
            for i in range(len(edges2)):
                edges2[i] += np #add point offset
        
        data['edges'] += edges2
    if 'edgeColor' in g1:
        data['edgeColor'] = copy.copy(g1['edgeColor']) #only taken from g1
    elif 'edgeColor' in g2:
        data['edgeColor'] = copy.copy(g2['edgeColor']) #only taken from g1

    for p in g2['triangles']:
        data['triangles'] += [int(p + np)] #add point offset for correct connectivity

    return data


#************************************************
#**function: generate graphics data for lines, given by list of points and color; transforms to GraphicsData dictionary
#**input: 
#  pList: list of 3D numpy arrays or lists (to achieve closed curve, set last point equal to first point)
#  color: provided as list of 4 RGBA values
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
#**example:
##create simple 3-point lines
#gLine=GraphicsDataLine([[0,0,0],[1,0,0],[2,0.5,0]], color=color4red)
def GraphicsDataLine(pList, color=[0.,0.,0.,1.]): 
    data = [0]*(len(pList)*3)
    for i, p in enumerate(pList):
        data[i*3:i*3+3] = list(p)
    dataRect = {'type':'Line', 'color': list(color), 'data':data}

    return dataRect

#************************************************
#**function: generate graphics data for a single circle; currently the plane normal = [0,0,1], just allowing to draw planar circles -- this may be extended in future!
#**input: 
#  point: center point of circle
#  radius: radius of circle
#  color: provided as list of 4 RGBA values
#**notes: the tiling (number of segments to draw circle) can be adjusted by visualizationSettings.general.circleTiling
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataCircle(point=[0,0,0], radius=1, color=[0.,0.,0.,1.]): 
    return {'type':'Circle', 'color': list(color), 'radius': radius, 'position':list(point)}

#************************************************
#**function: generate graphics data for a text drawn at a 3D position
#**input: 
#  point: position of text
#  text: string representing text
#  color: provided as list of 4 RGBA values
#**nodes: text size can be adjusted with visualizationSettings.general.textSize, which affects the text size (=font size) globally
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataText(point=[0,0,0], text='', color=[0.,0.,0.,1.]): 
    return {'type':'Text', 'color': list(color), 'text':text, 'position':list(point)}

#************************************************
#**function: generate graphics data for 2D rectangle
#**input: minimal and maximal cartesian coordinates in (x/y) plane; color provided as list of 4 RGBA values
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataRectangle(xMin, yMin, xMax, yMax, color=[0.,0.,0.,1.]): 

    rect = [xMin, yMin,xMax,yMax]
    dataRect = {'type':'Line', 'color': list(color), 'data':[rect[0],rect[1],0, rect[2],rect[1],0, rect[2],rect[3],0, rect[0],rect[3],0, rect[0],rect[1],0]}

    return dataRect

#************************************************
#**function: generate graphics data for orthogonal block drawn with lines
#**input: minimal and maximal cartesian coordinates for orthogonal cube; color provided as list of 4 RGBA values
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataOrthoCubeLines(xMin, yMin, zMin, xMax, yMax, zMax, color=[0.,0.,0.,1.]): 

    dataRect = {'type':'Line', 'color': list(color), 'data':[xMin,yMin,zMin, xMin,yMax,zMin, xMin,yMin,zMin, xMax,yMin,zMin, xMax,yMax,zMin, xMax,yMin,zMin, 
                                                       xMax,yMin,zMax, xMax,yMax,zMax, xMax,yMin,zMax, xMin,yMin,zMax, xMin,yMax,zMax, xMin,yMin,zMax, 
                                                       xMin,yMin,zMin, xMin,yMax,zMin, xMax,yMax,zMin, xMax,yMax,zMax, xMin,yMax,zMax, xMin,yMax,zMin]}

    return dataRect

#**function: generate graphics data for orthogonal 3D block with min and max dimensions
#**input: 
#  x/y/z/Min/Max: minimal and maximal cartesian coordinates for orthogonal cube
#  color: list of 4 RGBA values
#  addNormals: add face normals to triangle information
#  addEdges: if True, edges are added in TriangleList of GraphicsData 
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataOrthoCube(xMin, yMin, zMin, xMax, yMax, zMax, color=[0.,0.,0.,1.], addNormals=False, addEdges=False, edgeColor=color4black, addFaces=True): 
    
    pList = [[xMin,yMin,zMin], [xMax,yMin,zMin], [xMax,yMax,zMin], [xMin,yMax,zMin],
             [xMin,yMin,zMax], [xMax,yMin,zMax], [xMax,yMax,zMax], [xMin,yMax,zMax]]
    return GraphicsDataCube(pList, list(color), addNormals=addNormals, addEdges=addEdges, edgeColor=edgeColor, addFaces=addFaces)

#**function: generate graphics data forfor orthogonal 3D block with center point and size
#**input: 
#  centerPoint: center of cube as 3D list or np.array
#  size: size as 3D list or np.array
#  color: list of 4 RGBA values
#  addNormals: add face normals to triangle information
#  addEdges: if True, edges are added in TriangleList of GraphicsData 
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects; if addEdges=True, it returns a list of two dictionaries
def GraphicsDataOrthoCubePoint(centerPoint=[0,0,0], size=[0.1,0.1,0.1], color=[0.,0.,0.,1.], addNormals=False, addEdges=False, edgeColor=color4black, addFaces=True): 
    
    xMin = centerPoint[0] - 0.5*size[0]
    yMin = centerPoint[1] - 0.5*size[1]
    zMin = centerPoint[2] - 0.5*size[2]
    xMax = centerPoint[0] + 0.5*size[0]
    yMax = centerPoint[1] + 0.5*size[1]
    zMax = centerPoint[2] + 0.5*size[2]

    gCube = GraphicsDataOrthoCube(xMin, yMin, zMin, xMax, yMax, zMax, color, 
                                  addNormals=addNormals, addEdges=addEdges, edgeColor=edgeColor, addFaces=addFaces)
    if addEdges:
        gCube['edgeColor'] = list(edgeColor)
        gCube['edges'] = [0,1, 1,2, 2,3, 3,0,  0,4, 1,5, 2,6, 3,7,  4,5, 5,6, 6,7, 7,4]
        #print('new2')
    return gCube

#**function: generate graphics data for general block with endpoints, according to given vertex definition
#**input: 
#  pList: is a list of points [[x0,y0,z0],[x1,y1,z1],...]
#  color: provided as list of 4 RGBA values
#  faces: includes the list of six binary values (0/1), denoting active faces (value=1); set index to zero to hide face
#  addNormals: if True, normals are added and there are separate points for every triangle
#  addEdges: if True, edges are added in TriangleList of GraphicsData 
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataCube(pList, color=[0.,0.,0.,1.], faces=[1,1,1,1,1,1], addNormals=False, addEdges=False, edgeColor=color4black, addFaces=True): 
# bottom: (z goes upwards from node 0 to node 4)
# ^y
# |
# 3---2
# |   |
# |   |
# 0---1-->x
#
# top:
# ^y
# |
# 7---6
# |   |
# |   |
# 4---5-->x
#
# faces: bottom, top, sideface0, sideface1, sideface2, sideface3 (sideface0 has nodes 0,1,4,5)

    colors=[]
    for i in range(8):
        colors=colors+color

    points = []
    for p in pList:
        points += p
#    points = [xMin,yMin,zMin, xMax,yMin,zMin, xMax,yMax,zMin, xMin,yMax,zMin,
#              xMin,yMin,zMax, xMax,yMin,zMax, xMax,yMax,zMax, xMin,yMax,zMax]

    #1-based ... triangles = [1,3,2, 1,4,3, 5,6,7, 5,7,8, 1,2,5, 2,6,5, 2,3,6, 3,7,6, 3,4,7, 4,8,7, 4,1,8, 1,5,8 ]
    #triangles = [0,2,1, 0,3,2, 6,4,5, 6,7,4, 0,1,4, 1,5,4, 1,2,5, 2,6,5, 2,3,6, 3,7,6, 3,0,7, 0,4,7]

    trigList = [[0,2,1], [0,3,2], #
                [6,4,5], [6,7,4], #
                [0,1,4], [1,5,4], #
                [1,2,5], [2,6,5], #
                [2,3,6], [3,7,6], #
                [3,0,7], [0,4,7]] #
    triangles = []
    # print('addNormals=',addNormals)
    if not addNormals:
        for i in range(6):
            if faces[i]:
                for j in range(2):
                    if addFaces:
                        triangles += trigList[i*2+j]
        data = {'type':'TriangleList', 'colors': colors, 'points':points, 'triangles':triangles}
    else:
        normals = []
        points2 = []
        
        cnt = 0
        for i in range(6):
            if faces[i]:
                for j in range(2):
                    trig = trigList[i*2+j]
                    normal = ComputeTriangleNormal(pList[trig[0]],pList[trig[1]],pList[trig[2]])
                    normals+=list(normal)*3 #add normal for every point
                    for k in range(3):
                        if addFaces:
                            triangles += [cnt] #new point for every triangle
                        points2 += list(pList[trig[k]])
                        cnt+=1
        
        data = {'type':'TriangleList', 'colors': color*cnt, 'normals':normals, 'points':points2, 'triangles':triangles}

    if addEdges:
        edges = [0,1, 1,2, 2,3, 3,0,
                 4,5, 5,6, 6,7, 7,4,
                 0,4, 1,5, 2,6, 3,7 ]
        
        data['edges'] = edges
        data['edgeColor'] = list(edgeColor)
        
    return data

#**function: generate graphics data for a sphere with point p and radius
#**input:
#  point: center of sphere (3D list or np.array)
#  radius: positive value
#  color: provided as list of 4 RGBA values
#  nTiles: used to determine resolution of sphere >=3; use larger values for finer resolution
#  addEdges: True or number of edges along sphere shell (under development); for optimal drawing, nTiles shall be multiple of 4 or 8
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataSphere(point=[0,0,0], radius=0.1, color=[0.,0.,0.,1.], nTiles = 8, 
                       addEdges = False, edgeColor=color4black, addFaces=True):
    if nTiles < 3: print("WARNING: GraphicsDataSphere: nTiles < 3: set nTiles=3")
    
    p = np.array(point)
    r = radius
    #orthonormal basis:
    e0=np.array([1,0,0])
    e1=np.array([0,1,0])
    e2=np.array([0,0,1])

    points = []
    normals = []
    colors = []
    triangles = []
    
    #create points for circles around z-axis with tiling
    for i0 in range(nTiles+1):
        for iphi in range(nTiles):
            z = -r*cos(pi*i0/nTiles)    #runs from -r .. r (this is the coordinate of the axis of circles)
            phi = 2*pi*iphi/nTiles #angle
            fact = sin(pi*i0/nTiles)

            x = fact*r*sin(phi)
            y = fact*r*cos(phi)

            vv = x*e0 + y*e1 + z*e2
            points += list(p + vv)
            
            n = ebu.Normalize(vv) #2022-06-27: corrected to (vv) to point outwards
            #print(n)
            normals += n
            
            colors += color

    
    if addFaces:
        for i0 in range(nTiles):
            for iphi in range(nTiles):
                p0 = i0*nTiles+iphi
                p1 = (i0+1)*nTiles+iphi
                iphi1 = iphi + 1
                if iphi1 >= nTiles: 
                    iphi1 = 0
                p2 = i0*nTiles+iphi1
                p3 = (i0+1)*nTiles+iphi1
    
                if switchTriangleOrder:
                    triangles += [p0,p3,p1, p0,p2,p3]
                else:
                    triangles += [p0,p1,p3, p0,p3,p2]
            
    data = {'type':'TriangleList', 'colors':colors, 
            'normals':normals, 
            'points':points, 
            'triangles':triangles}
    
    if type(addEdges) == bool and addEdges == True:
        addEdges = 3

    if addEdges > 0:
        data['edgeColor'] = list(edgeColor)

        edges = []
        hEdges = [] #edges at half of iphi
        nt = 2
        if addEdges > 1:
            nt = 4
        if addEdges > 3:
            nt = 8
        for j in range(nt):
            hEdges += [[]]
        hTiles = int(nTiles/nt)
        # hLast = [None]*nt
        # hFirst = [None]*nt
        sTiles = max(addEdges-1,1) #non-negative
        nStep = int(nTiles/sTiles)
        
        for i0 in range(nTiles):
            for iphi in range(nTiles):
                p0 = i0*nTiles+iphi
                p1 = (i0+1)*nTiles+iphi
                if i0%nStep == 0:
                    iphi1 = iphi + 1
                    if iphi1 >= nTiles: 
                        iphi1 = 0
                    p2 = i0*nTiles+iphi1
                    if addEdges>1:
                        edges += [p0, p2]
                if hTiles != 0:
                    if iphi%hTiles == 0:
                        j = int(iphi/hTiles)
                        if j < nt:
                            hEdges[j] += [p0,p1]
                            # if hLast[j] == None:
                            #     hLast[j] = p0
                            #     hFirst[j] = p0
                            # else:
                            #     hEdges[j] += [hLast[j], p0]
                            #     hLast[j] = p0
        
        for j in range(nt):
            #print('j=',j, hEdges[j], ', hFirst=',hFirst)
            if nt%2 == 0: #close edges only for even nt
                hEdges[j] += [hEdges[j][-1], hEdges[(j+int(nt/2))%nt][-1]]
                
            edges += hEdges[j]

        data['edges'] = edges
    
    return data
            
#**function: generate graphics data for a cylinder with given axis, radius and color; nTiles gives the number of tiles (minimum=3)
#**input:
#  pAxis: axis point of one face of cylinder (3D list or np.array)
#  vAxis: vector representing the cylinder's axis (3D list or np.array)
#  radius: positive value representing radius of cylinder
#  color: provided as list of 4 RGBA values
#  nTiles: used to determine resolution of cylinder >=3; use larger values for finer resolution
#  angleRange: given in rad, to draw only part of cylinder (halfcylinder, etc.); for full range use [0..2 * pi]
#  lastFace: if angleRange != [0,2*pi], then the faces of the open cylinder are shown with lastFace = True
#  cutPlain: only used for angleRange != [0,2*pi]; if True, a plane is cut through the part of the cylinder; if False, the cylinder becomes a cake shape ...
#  addEdges: if True, edges are added in TriangleList of GraphicsData; if addEdges is integer, additional int(addEdges) lines are added on the cylinder mantle
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#  alternatingColor: if given, optionally another color in order to see rotation of solid; only works, if angleRange=[0,2*pi]
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataCylinder(pAxis=[0,0,0], vAxis=[0,0,1], radius=0.1, color=[0.,0.,0.,1.], nTiles = 16, 
                         angleRange=[0,2*pi], lastFace = True, cutPlain = True, 
                         addEdges=False, edgeColor=color4black,
                         addFaces=True, **kwargs):  

    if nTiles < 3: print("WARNING: GraphicsDataCylinder: nTiles < 3: set nTiles=3")
    
    #create points at left and right face
    points0=list(pAxis) #[pAxis[0],pAxis[1],pAxis[2]] #avoid change of pAxis
    pAxis1=[pAxis[0]+vAxis[0],pAxis[1]+vAxis[1],pAxis[2]+vAxis[2]]
    points1=list(pAxis1) #[pAxis[0]+vAxis[0],pAxis[1]+vAxis[1],pAxis[2]+vAxis[2]] #copy in order to avoid change of pAxis1 for use lateron
    
    p0 = np.array(pAxis)
    p1 = np.array(pAxis) + np.array(vAxis)
    
    basis = ComputeOrthonormalBasisVectors(vAxis)
    #v0 = basis[0]
    n1 = basis[1]
    n2 = basis[2]
    r=radius
    
    nf = normalsFactor #-1 original; -1 points inside

    #create normals at left and right face (pointing inwards)
    normals0 = ebu.Normalize([-vAxis[0],-vAxis[1],-vAxis[2]])
    normals1 = ebu.Normalize(vAxis)

    points2 = []
    points3 = []
    
    alpha = angleRange[1]-angleRange[0] #angular range
    alpha0 = angleRange[0]

    fact = nTiles #create correct part of cylinder
    if alpha < 2.*pi: 
        fact = nTiles-1

    # pointsCyl0 = []
    # pointsCyl1 = []
    
    for i in range(nTiles):
        phi = alpha0 + i*alpha/fact
        x = r*sin(phi)
        y = r*cos(phi)
        vv = x*n1 + y*n2
        pz0 = p0 + vv
        pz1 = p1 + vv
        points0 += list(pz0)
        points1 += list(pz1)
        points2 += list(pz0) #other points for side faces (different normals)
        points3 += list(pz1) #other points for side faces (different normals)
        # pointsCyl0 += list(pz0) #for edges
        # pointsCyl1 += list(pz1) #for edges
        n = ebu.Normalize(list(nf*vv))
        normals0 = normals0 + n
        normals1 = normals1 + n
        
    
    points0 += points1+points2+points3
    normals0 += normals1

    for i in range(nTiles):
        normals0 += ebu.Normalize([-nf*vAxis[0],-nf*vAxis[1],-nf*vAxis[2]])
    for i in range(nTiles):
        normals0 += ebu.Normalize([nf*vAxis[0],nf*vAxis[1],nf*vAxis[2]])

    n = nTiles+1 #number of points of one ring+midpoint
    color2 = list(color) #alternating color
    if 'alternatingColor' in kwargs:
        color2 = kwargs['alternatingColor']

    colors=[]
    #for i in range(2*n+2*nTiles):
    #    colors += color
    n2 = int(nTiles/2)    
    for i in range(2):
        colors += color
    for j in range(4):
        for i in range(n2):
            colors += color
        for i in range(nTiles-n2):
            colors += color2

    triangles = []
    #circumference:
    for i in range(nTiles):
        if switchTriangleOrder:
            if i != nTiles-1:
                triangles += [1+i,n+1+i+1,n+1+i]
                triangles += [1+i,1+i+1,n+1+i+1]
            else:
                if lastFace and cutPlain:
                    triangles += [1+i,n+1,n+1+i]
                    triangles += [1+i,1,n+1]
        else:
            if i != nTiles-1:
                triangles += [1+i,n+1+i,n+1+i+1]
                triangles += [1+i,n+1+i+1,1+i+1]
            else:
                if lastFace and cutPlain:
                    triangles += [1+i,n+1+i,n+1]
                    triangles += [1+i,n+1,1]
            
    #sides faces left and right:
    nn=2*n #offset
    for i in range(nTiles):
        if switchTriangleOrder:
            if i != nTiles-1:
                triangles += [0,nn+i,nn+i+1]
                triangles += [n,nn+nTiles+i+1,nn+nTiles+i]
            else:
                if cutPlain:
                    triangles += [0,nn+i,nn]
                    triangles += [n,nn+nTiles,nn+nTiles+i]
        else:
            if i != nTiles-1:
                triangles += [0,nn+i,nn+i+1]
                triangles += [n,nn+nTiles+i+1,nn+nTiles+i]
            else:
                if cutPlain:
                    triangles += [0,nn+i,nn]
                    triangles += [n,nn+nTiles,nn+nTiles+i]

    #if angles are not 2*pi, add closing face
    if lastFace and not(cutPlain):
        s = int(len(points0)/3) #starting index for side triangles
        p2 = points2[0:3]
        p3 = points3[0:3]
        p4 = points2[len(points2)-3:len(points2)]
        p5 = points3[len(points3)-3:len(points3)]
        points0 += pAxis + pAxis1 + p2 + p3 + pAxis + pAxis1 + p4 + p5
        n1=np.cross(ebu.VSub(pAxis,pAxis1),ebu.VSub(p3,pAxis))
        n1=list(ebu.Normalize(-nf*n1))
        n2=np.cross(ebu.VSub(pAxis1,pAxis),ebu.VSub(p4,pAxis))
        n2=list(ebu.Normalize(-nf*n2))
        normals0 += n1+n1+n1+n1+n2+n2+n2+n2  #8 additional normals
        if switchTriangleOrder:
            triangles += [s+0,s+3,s+1, s+0,s+2,s+3, 
                          s+5,s+6,s+4, s+5,s+7,s+6]
        else:
            triangles += [s+0,s+1,s+3, s+0,s+3,s+2, 
                          s+5,s+4,s+6, s+5,s+6,s+7]
            
        for i in range(8): #8 additional colors
            colors += color

    # print('points len=', len(points0))
    # print('normals len=', len(normals0))
    if not addFaces:
        triangles = []

    #triangle normals point inwards to object ...
    data = {'type':'TriangleList', 'colors':colors, 
            'normals':normals0, 
            'points':points0, 'triangles':triangles}

    if addEdges:
        data['edgeColor'] = list(edgeColor)
        
        faceEdges = 0
        if type(addEdges) != bool:
            faceEdges = int(addEdges)
        
        edges = []
        pLast = nTiles
        for i in range(nTiles):
            edges += [pLast, i+1]
            pLast = i+1
        
        pLast = nTiles + (nTiles+1)
        for i in range(nTiles):
            edges += [pLast, i+1+(nTiles+1)]
            pLast = i+1+(nTiles+1)
        
        if faceEdges > 0:
            nStep = int(nTiles/faceEdges)
            pLast0 = 1
            pLast1 = 1+(nTiles+1)
            for i in range(faceEdges):
                edges += [pLast0, pLast1]
                pLast0 += nStep
                pLast1 += nStep
        
        data['edges'] = edges

    return data

#**function: generate graphics data for a planar Link between the two joint positions, having two axes
#**input:
#  p0: joint0 center position
#  p1: joint1 center position
#  axis0: direction of rotation axis at p0, if drawn as a cylinder; [0,0,0] otherwise
#  axis1: direction of rotation axis of p1, if drawn as a cylinder; [0,0,0] otherwise
#  radius: list of two radii [radius0, radius1], being the two radii of the joints drawn by a cylinder or sphere    
#  width: list of two widths [width0, width1], being the two widths of the joints drawn by a cylinder; ignored for sphere    
#  thickness: the thickness of the link (shaft) between the two joint positions; thickness in z-direction or diameter (cylinder)
#  color: provided as list of 4 RGBA values
#  nTiles: used to determine resolution of cylinder >=3; use larger values for finer resolution
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataRigidLink(p0,p1,axis0=[0,0,0], axis1=[0,0,0], radius=[0.1,0.1], 
                          thickness=0.05, width=[0.05,0.05], color=[0.,0.,0.,1.], nTiles = 16):
    linkAxis = ebu.VSub(p1,p0)
    #linkAxis0 = ebu.Normalize(linkAxis)
    a0=list(axis0)
    a1=list(axis1)
    
    data0 = GraphicsDataCylinder(p0, linkAxis, 0.5*thickness, color, nTiles)
    data1 = {}
    data2 = {}

    if ebu.NormL2(axis0) == 0:
        data1 = GraphicsDataSphere(p0, radius[0], color, nTiles)
    else:
        a0=ebu.Normalize(a0)
        data1 = GraphicsDataCylinder(list(np.array(p0)-0.5*width[0]*np.array(a0)), 
                                     list(width[0]*np.array(a0)), 
                                     radius[0], color, nTiles)
        
    if ebu.NormL2(axis1) == 0:
        data2 = GraphicsDataSphere(p1, radius[1], color, nTiles)
    else:
        a1=ebu.Normalize(a1)
        data2 = GraphicsDataCylinder(list(np.array(p1)-0.5*width[1]*np.array(a1)), 
                                     list(width[1]*np.array(a1)), radius[1], color, nTiles)

    #now merge lists, including appropriate indices of triangle points!
    np0 = int(len(data0['points'])/3) #number of points of first point list ==> this is the offset for next list
    np1 = np0 + int(len(data1['points'])/3) #number of points of first point list ==> this is the offset for next list

    triangles = data0['triangles']
    trigs1 = np.array(data1['triangles'])
    trigs1 += np0
    triangles += list(trigs1)
    
    trigs2 = np.array(data2['triangles'])
    trigs2 += np1
    triangles += list(trigs2)
    
    points = data0['points'] + data1['points'] + data2['points']
    normals = data0['normals'] + data1['normals'] + data2['normals']
    colors = data0['colors'] + data1['colors'] + data2['colors']
    
    data = {'type':'TriangleList', 'colors':colors, 
            'normals':normals, 
            'points':points, 'triangles':triangles}
    return data


#**function: generate graphics data from STL file (text format!) and use color for visualization; this function is slow, use stl binary files with GraphicsDataFromSTLfile(...)
#**input:
#  fileName: string containing directory and filename of STL-file (in text / SCII format) to load
#  color: provided as list of 4 RGBA values
#  verbose: if True, useful information is provided during reading
#  invertNormals: if True, orientation of normals (usually pointing inwards in STL mesh) are inverted for compatibility in Exudyn
#  invertTriangles: if True, triangle orientation (based on local indices) is inverted for compatibility in Exudyn
#**output: creates graphicsData, inverting the STL graphics regarding normals and triangle orientations (interchanged 2nd and 3rd component of triangle index)
def GraphicsDataFromSTLfileTxt(fileName, color=[0.,0.,0.,1.], verbose=False, invertNormals=True, invertTriangles=True): 
#file format, just one triangle, using GOMinspect:
#solid solidName
#facet normal -0.979434 0.000138 -0.201766
# outer loop
#    vertex 9.237351 7.700452 -9.816338
#    vertex 9.237478 10.187849 -9.815249
#    vertex 9.706021 10.170116 -12.089709
# endloop
#endfacet
#...
#endsolid solidName
    if verbose: print("read STL file: "+fileName)

    fileLines = []
    try: #still close file if crashes
        file=open(fileName,'r') 
        fileLines = file.readlines()
    finally:
        file.close()    

    colors=[]
    points = []
    normals = []
    triangles = []

    nf = 1.-2.*int(invertNormals) #+1 or -1 (inverted)
    indOff = int(invertTriangles) #0 or 1 (inverted)

    nLines = len(fileLines)
    lineCnt = 0
    if fileLines[lineCnt][0:5] != 'solid':
        raise ValueError("GraphicsDataFromSTLfileTxt: expected 'solid ...' in first line, but received: " + fileLines[lineCnt])
    lineCnt+=1
    
    if nLines > 500000:
        print('large ascii STL file; switch to numpy-stl and binary format for faster loading!')

    while lineCnt < nLines and fileLines[lineCnt].strip().split()[0] != 'endsolid':
        if lineCnt%100000 == 0 and lineCnt !=0: 
            if verbose: print("  read line",lineCnt," / ", len(fileLines))

        normalLine = fileLines[lineCnt].split()
        if normalLine[0] != 'facet' or normalLine[1] != 'normal':
            raise ValueError("GraphicsDataFromSTLfileTxt: expected 'facet normal ...' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])
        if len(normalLine) != 5:
            raise ValueError("GraphicsDataFromSTLfileTxt: expected 'facet normal n0 n1 n2' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])
        
        normal = [nf*float(normalLine[2]),nf*float(normalLine[3]),nf*float(normalLine[4])]

        lineCnt+=1
        loopLine = fileLines[lineCnt].strip()
        if loopLine != 'outer loop':
            raise ValueError("GraphicsDataFromSTLfileTxt: expected 'outer loop' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])

        ind = int(len(points)/3) #index for points of this triangle
        #get 3 vertices:
        lineCnt+=1
        for i in range(3):
            readLine = fileLines[lineCnt].strip().split()
            if readLine[0] != 'vertex':
                raise ValueError("GraphicsDataFromSTLfileTxt: expected 'vertex ...' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])
            if len(readLine) != 4:
                raise ValueError("GraphicsDataFromSTLfileTxt: expected 'vertex v0 v1 v2' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])
            
            points+=[float(readLine[1]),float(readLine[2]),float(readLine[3])]
            normals+=normal
            colors+=color
            lineCnt+=1
            
        triangles+=[ind,ind+1+indOff,ind+2-indOff] #indices of points; flip indices to match definition in EXUDYN

        loopLine = fileLines[lineCnt].strip()
        if loopLine != 'endloop':
            raise ValueError("GraphicsDataFromSTLfileTxt: expected 'endloop' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])
        lineCnt+=1
        loopLine = fileLines[lineCnt].strip()
        if loopLine != 'endfacet':
            raise ValueError("GraphicsDataFromSTLfileTxt: expected 'endfacet' in line "+str(lineCnt)+", but received: " + fileLines[lineCnt])
        lineCnt+=1
    
    data = {'type':'TriangleList', 'colors':colors, 'normals':normals, 'points':points, 'triangles':triangles}
    return data


#%%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#**function: generate graphics data from STL file, allowing text or binary format; requires numpy-stl to be installed; additionally can scale, rotate and translate
#**input:
#  fileName: string containing directory and filename of STL-file (in text / SCII format) to load
#  color: provided as list of 4 RGBA values
#  verbose: if True, useful information is provided during reading
#  density: if given and if verbose, mass, volume, inertia, etc. are computed
#  scale: point coordinates are transformed by scaling factor
#  invertNormals: if True, orientation of normals (usually pointing inwards in STL mesh) are inverted for compatibility in Exudyn
#  invertTriangles: if True, triangle orientation (based on local indices) is inverted for compatibility in Exudyn
#**output: creates graphicsData, inverting the STL graphics regarding normals and triangle orientations (interchanged 2nd and 3rd component of triangle index)
#**notes: the model is first scaled, then rotated, then the offset pOff is added; finally min, max, mass, volume, inertia, com are computed!
def GraphicsDataFromSTLfile(fileName, color=[0.,0.,0.,1.], verbose=False, density=0., scale=1., Aoff=[], pOff=[], invertNormals=True, invertTriangles=True):
    
    try:
        from stl import mesh
    except:
        raise ValueError('GraphicsDataFromSTLfile requires installation of numpy-stl; try "pip install numpy-stl"')
    
    data=mesh.Mesh.from_file(fileName)
    nPoints = 3*len(data.points) #data.points has shape (nTrigs,9), one triangle has 3 points!
    
    if scale != 1.:
        data.points *= scale
    
    p = copy.copy(pOff)
    A = copy.deepcopy(Aoff) #deepcopy for list of lists
    
    if p != [] or A != []:
        from exudyn.rigidBodyUtilities import HomogeneousTransformation
        if p == []: p=[0,0,0]
        if A == []: A=np.eye(3)
        HT = HomogeneousTransformation(A, p)
        
        data.transform(HT)
        
    dictData = {}
    if verbose:
        print('GraphicsDataFromSTLfile:')
        print('  max point=', list(data.max_))
        print('  min point=', list(data.min_))
        print('  STL points=', nPoints)
    if density != 0:
        [volume, mass, COM, inertia] = data.get_mass_properties_with_density(density)
        dictData = {'minPos':data.min_,
                    'maxPos':data.max_,
                    'volume':volume,
                    'mass':mass,
                    'COM':COM,
                    'inertia':inertia
                    }
    if verbose:
        print('  volume =', volume)
        print('  center of mass =', list(COM))
        print('  inertia =', list(inertia))
    
    # print('STL points3=', nPoints3)
    
    colors = color*nPoints
    #triangles = list(np.arange(0,nPoints))#wrong orientation ==> reverse
    if invertTriangles:
        triangles = list(np.arange(nPoints-1,-1,-1))#inverted sorting
    else:
        triangles = list(np.arange(0,nPoints))      #unmodified sorting of indices
    points = list(data.points.flatten())
    nf = 1.-2.*int(invertNormals) #+1 or -1 (inverted)
    normals = list(np.kron([nf,nf,nf],data.normals).flatten()) #normals must be per point

    dictGraphics = {'type':'TriangleList', 'colors':colors, 'normals':normals, 'points':points, 'triangles':triangles}
    if density == 0:
        return dictGraphics 
    else:
        return [dictGraphics, dictData]


#**function: compute and return GraphicsData with edges and smoothend normals for mesh consisting of points and triangles (e.g., as returned from GraphicsData2PointsAndTrigs)
#  graphicsData: single GraphicsData object of type TriangleList; existing edges are ignored
#  edgeColor: optional color for edges
#  edgeAngle: angle above which edges are added to geometry
#  roundDigits: number of digits, relative to max dimensions of object, at which points are assumed to be equal
#  smoothNormals: if True, algorithm tries to smoothen normals at vertices; otherwise, uses triangle normals
#  addEdges: if True, edges are added in TriangleList of GraphicsData 
#  triangleColor: if triangleColor is set to a RGBA color, this color is used for the new triangle mesh throughout
#**output: returns GraphicsData with added edges and smoothed normals
#**notes: this function is suitable for STL import; it assumes that all colors in graphicsData are the same and only takes the first color!
def AddEdgesAndSmoothenNormals(graphicsData, edgeColor = color4black, edgeAngle = 0.25*pi,
                           pointTolerance=5, addEdges=True, smoothNormals=True, roundDigits=5, 
                           triangleColor = []):
    from math import acos # ,sin, cos

    oldColors = copy.copy(graphicsData['colors']) #2022-12-06: accepts now all colors; graphicsData['colors'][0:4]    
    [points, trigs]=GraphicsData2PointsAndTrigs(graphicsData)
    # [points, trigs]=RefineMesh(points, trigs)

    nPoints = len(points)
    nColors = int(len(oldColors)/4)

    triangleColorNew = list(triangleColor)

    if nColors != nPoints:
        print('WARNING: AddEdgesAndSmoothenNormals: found inconsistent colors; they must match the point list in graphics data')
        if triangleColorNew == []:
            triangleColorNew = graphicsData['colors'][0:4]

    if len(triangleColorNew) != 4 and len(triangleColorNew) != 0:
        triangleColorNew = [1,0,0,1]
        print('WARNING: AddEdgesAndSmoothenNormals: colors invalid; using default')

    if len(triangleColorNew) == 4:
        oldColors = list(triangleColorNew)*nPoints

    colors = [np.zeros(4)]*nPoints
    for i in range(nPoints):
        colors[i] = np.array(oldColors[i*4:i*4+4])
    
    points = np.array(points)
    trigs = np.array(trigs)
    colors = np.array(colors)
    pMax = np.max(points, axis=0)
    pMin = np.min(points, axis=0)
    maxDim = np.linalg.norm(pMax-pMin)
    if maxDim == 0: maxDim = 1.

    points = maxDim * np.round(points*(1./maxDim),roundDigits)
    # print('smoothen np=', nPoints)
    
    sortIndices = np.lexsort((points[:,2], points[:,1], points[:,0]))
    #sortedPoints = points[sortIndices]
    
    #now eliminate duplicate points:
    remap = np.zeros(nPoints,dtype=int)#np.int64)
    remap[0] = 0
    newPoints = [points[sortIndices[0],:]] #first point
    newColors = [colors[sortIndices[0],:]]
    
    cnt = 0
    for i in range(len(sortIndices)-1):
        nextIndex = sortIndices[i+1]
        if (points[nextIndex] != points[sortIndices[i]]).any():
            # newIndices.append(nextIndex)
            cnt+=1
            remap[nextIndex] = cnt#i+1
            newPoints.append(points[nextIndex,:])
            newColors.append(colors[nextIndex,:])
        else:
            remap[nextIndex] = cnt#newIndices[sortIndices[i]]
            # newIndices.append(newIndices[-1])
    newPoints = np.array(newPoints)
    newTrigs = remap[trigs]
    
    #==> now we (hopefully have connected triangle lists)
    
    nPoints = len(newPoints)
    nTrigs = len(newTrigs)
    
    #create points2trigs lists:
    points2trigs = [[] for i in range(nPoints)] #[[]]*nPoints does not work!!!!
    for cntTrig, trig in enumerate(newTrigs):
        for ind in trig:
            points2trigs[ind].append(cntTrig)
    
    #now find neighbours, compute triangle normals:
    neighbours = np.zeros((nTrigs,3),dtype=int)
    # neighbours[:,:] = -1#check if all neighbours found
    normals = np.zeros((nTrigs,3)) #per triangle
    areas = np.zeros(nTrigs)
    for cntTrig, trig in enumerate(newTrigs):
        normals[cntTrig,:] = ComputeTriangleNormal(newPoints[trig[0]], newPoints[trig[1]], newPoints[trig[2]])
        areas[cntTrig] = ComputeTriangleArea(newPoints[trig[0]], newPoints[trig[1]], newPoints[trig[2]])
        for cntNode in range(3):
            ind  = trig[cntNode]
            ind2 = trig[(cntNode+1)%3]
            for t in points2trigs[ind]:
                #if t <= cntTrig: continue #too much sorted out; check why
                trig2=newTrigs[t]
                found = False
                for cntNode2 in range(3):
                    if trig2[cntNode2] == ind2 and trig2[(cntNode2+1)%3] == ind:
                        neighbours[cntTrig, cntNode] = t
                        found = True
                        #print('neighbours ', cntTrig, t)
                        break
                if found: break
    
    #create edges:
    edges = [] #list of edge points
    pointHasEdge = [False]*nPoints
    for cntTrig, trig in enumerate(newTrigs):
        for cntNode in range(3):
            ind1  = trig[cntNode]
            ind2 = trig[(cntNode+1)%3]
            if ind1 > ind2:
                val = normals[cntTrig] @ normals[neighbours[cntTrig,cntNode]]
                if abs(val) > 1: val = np.sign(val) #because of float32 problems
                angle = acos(val)
                if angle >= edgeAngle:
                    edges+=[ind1, ind2]
                    pointHasEdge[ind1] = True
                    pointHasEdge[ind2] = True
    
    
    #smooth normals:
    #we simply do not smooth at points that have edges
    if smoothNormals:
        pointNormals = np.zeros((nPoints,3))
        for i in range(nPoints):
            if not pointHasEdge[i]:
                normal = np.zeros(3)
                for t in points2trigs[i]:
                    normal += areas[t]*normals[t]
                
                pointNormals[i] = ebu.Normalize(normal)

        
        finalTrigs = []
        newPoints = list(newPoints)
        newColors = list(newColors)
        pointNormals = list(pointNormals)
        for cnt, trig in enumerate(newTrigs):
            trigNew = [0,0,0]
            for i in range(3):
                if not pointHasEdge[trig[i]]:
                    trigNew[i] = trig[i]
                else:
                    trigNew[i] = len(newPoints)
                    newPoints.append(newPoints[trig[i]])
                    pointNormals.append(normals[cnt])
                    newColors.append(newColors[trig[i]])
            finalTrigs += [trigNew]
    else:
        finalTrigs = newTrigs
    
    graphicsData2 = GraphicsDataFromPointsAndTrigs(newPoints, finalTrigs, list(np.array(newColors).flatten()))
    if addEdges:
        graphicsData2['edges'] = edges
        graphicsData2['edgeColor'] = list(edgeColor)

    if smoothNormals:
        graphicsData2['normals'] = list(np.array(pointNormals).flatten())
    
    return graphicsData2

#**function: export given graphics data (only type TriangleList allowed!) to STL ascii file using fileName
#**input:
#  graphicsData: a single GraphicsData dictionary with type='TriangleList', no list of GraphicsData
#  fileName: file name including (local) path to export STL file
#  solidName: optional name used in STL file
#  invertNormals: if True, orientation of normals (usually pointing inwards in STL mesh) are inverted for compatibility in Exudyn
#  invertTriangles: if True, triangle orientation (based on local indices) is inverted for compatibility in Exudyn
def ExportGraphicsData2STL(graphicsData, fileName, solidName='ExudynSolid', invertNormals=True, invertTriangles=True):
    if graphicsData['type'] != 'TriangleList':
        raise ValueError('ExportGraphicsData2STL: invalid graphics data type; only TriangleList allowed')
        
    with open(fileName, 'w') as f:
        f.write('solid '+solidName+'\n')

        nTrig = int(len(graphicsData['triangles'])/3)
        triangles = graphicsData['triangles']
    
        for k in range(nTrig):
            p = [] #triangle points
            for i in range(3):
                ind = triangles[k*3+i]
                p += [np.array(graphicsData['points'][ind*3:ind*3+3])]
   
            n = ComputeTriangleNormal(p[0], p[1], p[2])
            
            f.write('facet normal '+str(-n[0]) + ' ' + str(-n[1]) + ' ' + str(-n[2]) + '\n') #normals inverted
            f.write('outer loop\n')
            f.write('vertex '+str(p[0][0]) + ' ' + str(p[0][1]) + ' ' + str(p[0][2]) + '\n')
            f.write('vertex '+str(p[2][0]) + ' ' + str(p[2][1]) + ' ' + str(p[2][2]) + '\n') #point index reversed!
            f.write('vertex '+str(p[1][0]) + ' ' + str(p[1][1]) + ' ' + str(p[1][2]) + '\n')
                
            f.write('endloop\n')
            f.write('endfacet\n')

        f.write('endsolid '+solidName+'\n')

            
    # data = {'type':'TriangleList', 'colors':colors, 
    #         'normals':normals, 
    #         'points':points, 'triangles':triangles}



#%%++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#   unused argument yet: contourNormals: if provided as list of 2D vectors, they prescribe the normals to the contour for smooth visualization; otherwise, contour is drawn flat
#**function: generate graphics data for a solid of revolution with given 3D point and axis, 2D point list for contour, (optional)2D normals and color; 
#**input:
#  pAxis: axis point of one face of solid of revolution (3D list or np.array)
#  vAxis: vector representing the solid of revolution's axis (3D list or np.array)
#  contour: a list of 2D-points, specifying the contour (x=axis, y=radius), e.g.: [[0,0],[0,0.1],[1,0.1]]
#  color: provided as list of 4 RGBA values
#  nTiles: used to determine resolution of solid; use larger values for finer resolution
#  smoothContour: if True, the contour is made smooth by auto-computing normals to the contour
#  addEdges: True or number of edges along revolution mantle; for optimal drawing, nTiles shall be multiple addEdges
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#  alternatingColor: add a second color, which enables to see the rotation of the solid
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
#**example:
##simple contour, using list of 2D points:
#contour=[[0,0.2],[0.3,0.2],[0.5,0.3],[0.7,0.4],[1,0.4],[1,0.]]
#rev1 = GraphicsDataSolidOfRevolution(pAxis=[0,0.5,0], vAxis=[1,0,0], 
#                                     contour=contour, color=color4red,
#                                     alternatingColor=color4grey)
##draw torus:
#contour=[]
#r = 0.2 #small radius of torus
#R = 0.5 #big radius of torus
#nc = 16 #discretization of torus
#for i in range(nc+3): #+3 in order to remove boundary effects
#    contour+=[[r*cos(i/nc*pi*2),R+r*sin(i/nc*pi*2)]]
#
##use smoothContour to make torus looking smooth
#rev2 = GraphicsDataSolidOfRevolution(pAxis=[0,0.5,0], vAxis=[1,0,0], 
#                                     contour=contour, color=color4red, 
#                                     nTiles = 64, smoothContour=True)
def GraphicsDataSolidOfRevolution(pAxis, vAxis, contour, color=[0.,0.,0.,1.], nTiles = 16, smoothContour = False, 
                                  addEdges = False, edgeColor=color4black, addFaces=True, **kwargs):  

    if len(contour) < 2: 
        raise ValueError("ERROR: GraphicsDataSolidOfRevolution: contour must contain at least 2 points")
    if nTiles < 3: 
        print("WARNING: GraphicsDataSolidOfRevolution: nTiles < 3: set nTiles=3")

    p0 = np.array(pAxis)
    #local coordinate system:
    [v,n1,n2] = ComputeOrthonormalBasisVectors(vAxis)

    color2 = list(color)
    if 'alternatingColor' in kwargs:
        color2 = kwargs['alternatingColor']

    #compute contour normals, assuming flat cones
    contourNormals = []
    for j in range(len(contour)-1):
        pc0 = np.array(contour[j])
        pc1 = np.array(contour[j+1])
        vc = pc1-pc0
        nc = ebu.Normalize([-vc[1],vc[0]])
        contourNormals += [nc]
    contourNormals += [contourNormals[-1]] #normal for last point same as previous

    if smoothContour:
        contourNormals2 = [contourNormals[0]]
        for j in range(len(contour)-1):
            ns = ebu.Normalize(np.array(contourNormals[j]) + np.array(contourNormals[j+1])) #not fully correct, but sufficient
            contourNormals2 += [list(ns)]
        contourNormals = contourNormals2

    points = []
    normals = []
    colors = []
    nT2 = int(nTiles/2)
    nf = normalsFactor #factor for normals (inwards/outwards)

    for j in range(len(contour)-1):
        pc0 = np.array(contour[j])
        pc1 = np.array(contour[j+1])
        points0 = []
        points1 = []
        normals0 = []
        normals1 = []
        for i in range(nTiles):
            phi = i*2*pi/nTiles
            x0 = pc0[1]*sin(phi)
            y0 = pc0[1]*cos(phi)
            vv0 = x0*n1 + y0*n2

            x1 = pc1[1]*sin(phi)
            y1 = pc1[1]*cos(phi)
            vv1 = x1*n1 + y1*n2

            pz0 = p0 + vv0 + pc0[0]*v
            pz1 = p0 + vv1 + pc1[0]*v
            points0 += list(pz0)
            points1 += list(pz1)

            #vc = pc1-pc0
            #nc = [-vc[1],vc[0]]
            nc0 = contourNormals[j]
            nUnit0 = ebu.Normalize(nf*nc0[1]*sin(phi)*n1 + nf*nc0[1]*cos(phi)*n2+nf*nc0[0]*v)
            nUnit1 = nUnit0
            if smoothContour:
                nc1 = contourNormals[j+1]
                nUnit1 = ebu.Normalize(nf*nc1[1]*sin(phi)*n1 + nf*nc1[1]*cos(phi)*n2+nf*nc1[0]*v)

            normals0 = normals0 + nUnit0
            normals1 = normals1 + nUnit1

        cList = list(color)*nT2 + list(color2)*(nTiles-nT2)
        colors += cList+cList
        points += points0 + points1
        normals += normals0 + normals1
    
    triangles = []
    n = nTiles
    #circumference:
    if addFaces:
        for j in range(len(contour)-1):
            k = j*2*n
            for i in range(nTiles):
                if i < nTiles-1:
                    triangles += [i+k,n+i+k+1,n+i+k]
                    triangles += [i+k,i+1+k,n+i+k+1]
                else:
                    triangles += [i+k,n+k,n+i+k]
                    triangles += [i+k,k,n+k]

    #triangle normals point inwards to object ...
    data = {'type':'TriangleList', 'colors':colors, 
            'normals':normals, 
            'points':points, 'triangles':triangles}


    if addEdges > 0:
        data['edgeColor'] = list(edgeColor)
        edges = []

        cntEdges = 0        
        nSteps = nTiles
        if type(addEdges) != bool and addEdges > 0:
            cntEdges = int(addEdges)
            nSteps = int(nTiles/cntEdges)
        
        hEdges = []
        for j in range(cntEdges):
            hEdges += [[]]

        for j in range(len(contour)-1):
            k = j*2*n
            for i in range(nTiles):
                edges += [i+k, (i+1)%nTiles+k]
                if i%nSteps==0:
                    j=int(i/nSteps)
                    if j < cntEdges:
                        hEdges[j] += [i+k, i+k+n]

        for j in range(cntEdges):
            edges += hEdges[j]

        data['edges'] = edges

    return data


#**function: generate graphics data for an arrow with given origin, axis, shaft radius, optional size factors for head and color; nTiles gives the number of tiles (minimum=3)
#**input:
#  pAxis: axis point of the origin (base) of the arrow (3D list or np.array)
#  vAxis: vector representing the vector pointing from the origin to the tip (head) of the error (3D list or np.array)
#  radius: positive value representing radius of shaft cylinder
#  headFactor: positive value representing the ratio between head's radius and the shaft radius
#  headStretch: positive value representing the ratio between the head's radius and the head's length
#  color: provided as list of 4 RGBA values
#  nTiles: used to determine resolution of arrow (of revolution object) >=3; use larger values for finer resolution
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataArrow(pAxis, vAxis, radius, color=[0.,0.,0.,1.], headFactor = 2, headStretch = 4, nTiles = 12):  
    L = ebu.NormL2(vAxis)
    rHead = radius * headFactor
    xHead = L - headStretch*rHead
    contour=[[0,0],[0,radius],[xHead,radius],[xHead,rHead],[L,0]]
    return GraphicsDataSolidOfRevolution(pAxis=pAxis, vAxis=vAxis, contour=contour, color=color, nTiles=nTiles)

#**function: generate graphics data for three arrows representing an orthogonal basis with point of origin, shaft radius, optional size factors for head and colors; nTiles gives the number of tiles (minimum=3)
#**input:
#  origin: point of the origin of the base (3D list or np.array)
#  rotationMatrix: optional transformation, which rotates the basis vectors
#  length: positive value representing lengths of arrows for basis
#  colors: provided as list of 3 colors (list of 4 RGBA values)
#  headFactor: positive value representing the ratio between head's radius and the shaft radius
#  headStretch: positive value representing the ratio between the head's radius and the head's length
#  nTiles: used to determine resolution of arrows of basis (of revolution object) >=3; use larger values for finer resolution
#  radius: positive value representing radius of arrows; default: radius = 0.01*length
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataBasis(origin=[0,0,0], rotationMatrix = np.eye(3), length = 1, colors=[color4red, color4green, color4blue], 
                      headFactor = 2, headStretch = 4, nTiles = 12, **kwargs):  
    radius = 0.01*length
    if 'radius' in kwargs:
        radius = kwargs['radius']

    A = np.array(rotationMatrix)
    g1 = GraphicsDataArrow(origin,A@[length,0,0],radius, colors[0], headFactor, headStretch, nTiles)
    g2 = GraphicsDataArrow(origin,A@[0,length,0],radius, colors[1], headFactor, headStretch, nTiles)
    g3 = GraphicsDataArrow(origin,A@[0,0,length],radius, colors[2], headFactor, headStretch, nTiles)

    return MergeGraphicsDataTriangleList(MergeGraphicsDataTriangleList(g1,g2),g3)

#**function: generate graphics data for frame (similar to GraphicsDataBasis), showing three arrows representing an orthogonal basis for the homogeneous transformation HT; optional shaft radius, optional size factors for head and colors; nTiles gives the number of tiles (minimum=3)
#**input:
#  HT: homogeneous transformation representing frame
#  length: positive value representing lengths of arrows for basis
#  colors: provided as list of 3 colors (list of 4 RGBA values)
#  headFactor: positive value representing the ratio between head's radius and the shaft radius
#  headStretch: positive value representing the ratio between the head's radius and the head's length
#  nTiles: used to determine resolution of arrows of basis (of revolution object) >=3; use larger values for finer resolution
#  radius: positive value representing radius of arrows; default: radius = 0.01*length
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataFrame(HT=np.eye(4), length = 1, colors=[color4red, color4green, color4blue], 
                      headFactor = 2, headStretch = 4, nTiles = 12, **kwargs):  
    radius = 0.01*length
    if 'radius' in kwargs:
        radius = kwargs['radius']

    
    A = HT2rotationMatrix(HT)
    origin = HT2translation(HT)
    
    g1 = GraphicsDataArrow(origin,A@[length,0,0],radius, colors[0], headFactor, headStretch, nTiles)
    g2 = GraphicsDataArrow(origin,A@[0,length,0],radius, colors[1], headFactor, headStretch, nTiles)
    g3 = GraphicsDataArrow(origin,A@[0,0,length],radius, colors[2], headFactor, headStretch, nTiles)

    return MergeGraphicsDataTriangleList(MergeGraphicsDataTriangleList(g1,g2),g3)


#**function: generate graphics data for simple quad with option for checkerboard pattern;
#  points are arranged counter-clock-wise, e.g.: p0=[0,0,0], p1=[1,0,0], p2=[1,1,0], p3=[0,1,0]
#**input: 
#  pList: list of 4 quad points [[x0,y0,z0],[x1,y1,z1],...]
#  color: provided as list of 4 RGBA values
#  alternatingColor: second color; if defined, a checkerboard pattern (default: 10x10) is drawn with color and alternatingColor
#  nTiles: number of tiles for checkerboard pattern (default: 10)
#  nTilesY: if defined, use number of tiles in y-direction different from x-direction (=nTiles)
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
#**example:
#plane = GraphicsDataQuad([[-8, 0, -8],[ 8, 0, -8,],[ 8, 0, 8],[-8, 0, 8]], 
#                         color4darkgrey, nTiles=8, 
#                         alternatingColor=color4lightgrey)
#oGround=mbs.AddObject(ObjectGround(referencePosition=[0,0,0],
#                      visualization=VObjectGround(graphicsData=[plane])))
def GraphicsDataQuad(pList, color=[0.,0.,0.,1.], **kwargs): 

    color2 = list(color)
    nTiles = 1
    if 'alternatingColor' in kwargs:
        color2 = kwargs['alternatingColor']
        nTiles = 10

    if 'nTiles' in kwargs:
        nTiles = kwargs['nTiles']
    nTilesY= nTiles
    if 'nTilesY' in kwargs:
        nTilesY = kwargs['nTilesY']

    p0 = np.array(pList[0])
    p1 = np.array(pList[1])
    p2 = np.array(pList[2])
    p3 = np.array(pList[3])

    points = []
    triangles = []
    #points are given always for 1 quad of checkerboard pattern
    ind = 0
    for j in range(nTilesY):
        for i in range(nTiles):
            f0 = j/(nTilesY)
            f1 = (j+1)/(nTilesY)
            pBottom0 = (nTiles-i)/nTiles  *((1-f0)*p0 + f0*p3) + (i)/nTiles  *((1-f0)*p1 + f0*p2)
            pBottom1 = (nTiles-i-1)/nTiles*((1-f0)*p0 + f0*p3) + (i+1)/nTiles*((1-f0)*p1 + f0*p2)
            pTop0 = (nTiles-i)/nTiles  *((1-f1)*p0 + f1*p3) + (i)/nTiles  *((1-f1)*p1 + f1*p2)
            pTop1 = (nTiles-i-1)/nTiles*((1-f1)*p0 + f1*p3) + (i+1)/nTiles*((1-f1)*p1 + f1*p2)
            points += list(pBottom0)+list(pBottom1)+list(pTop1)+list(pTop0)
            #points += list(p0)+list(p1)+list(p2)+list(p3)
            triangles += [0+ind,1+ind,2+ind,  0+ind,2+ind,3+ind]
            ind+=4

    colors=[]
    for j in range(nTilesY):
        for i in range(nTiles):
            a=1
            if i%2 == 1:
                a=-1
            if j%2 == 1:
                a=-1*a
            if a==1:
                c = list(color) #if no checkerboard pattern, just this color
            else:
                c = color2
            colors=colors+c+c+c+c #4 colors for one sub-quad

    data = {'type':'TriangleList', 'colors': colors, 'points':points, 'triangles':triangles}
    #print(data)
    return data


#**function: function to generate checkerboard background;
#  points are arranged counter-clock-wise, e.g.: 
#**input: 
#  point: midpoint of pattern provided as list or np.array
#  normal: normal to plane provided as list or np.array
#  size: dimension of first side length of quad
#  size2: dimension of second side length of quad
#  color: provided as list of 4 RGBA values
#  alternatingColor: second color; if defined, a checkerboard pattern (default: 10x10) is drawn with color and alternatingColor
#  nTiles: number of tiles for checkerboard pattern in first direction
#  nTiles2: number of tiles for checkerboard pattern in second direction; default: nTiles
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
#**example:
#plane = GraphicsDataCheckerBoard(normal=[0,0,1], size=5)
#oGround=mbs.AddObject(ObjectGround(referencePosition=[0,0,0],
#                      visualization=VObjectGround(graphicsData=[plane])))
def GraphicsDataCheckerBoard(point=[0,0,0], normal=[0,0,1], size = 1,
                             color=color4lightgrey, alternatingColor=color4lightgrey2, nTiles=10, **kwargs):
    nTiles2 = nTiles
    if 'nTiles2' in kwargs:
        nTiles2 = kwargs['nTiles2']
    size2 = size
    if 'size2' in kwargs:
        size2 = kwargs['size2']

    [v,n1,n2] = ComputeOrthonormalBasisVectors(normal)
    p0=np.array(point)
    points = [list(p0-0.5*size*n1-0.5*size2*n2),
              list(p0+0.5*size*n1-0.5*size2*n2),
              list(p0+0.5*size*n1+0.5*size2*n2),
              list(p0-0.5*size*n1+0.5*size2*n2)]

    return GraphicsDataQuad(points, color=list(color), alternatingColor=alternatingColor, 
                            nTiles=nTiles, nTilesY=nTiles2)

#%%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#**function: helper function to compute triangular mesh from list of vertices (=points) and segments;
#   computes triangular meshes for non-convex case. In order to make it efficient, it first computes
#   neighbors and then defines triangles at segments to be inside/outside. Finally neighboring
#   relations are used to define all triangles inside/outside
#   finally only returns triangles that are inside the segments
#**input:
#  vertices: list of pairs of coordinates of vertices in mesh [x,y]
#  segments: list of segments, which are pairs of node numbers [i,j], defining the boundary of the mesh;
#            the ordering of the nodes is such that left triangle = inside, right triangle = outside, compare example with segment [V1,V2]:\\
#  
#     inside
#  V1         V2
#  O----------O
#    outside
#**output:
#  triangulation structure of Delaunay(...), see scipy.spatial.Delaunaystructure, containing all simplices (=triangles)
#**notes: Delauney will not work if points are duplicated; you must first create point lists without duplicated points!
#**example:
# points = np.array([[0, 0], [0, 2], [2, 2], [2, 1], [1, 1], [0, 1], [1, 0]])
# segments = [len(points)-1,0]
# for i in range(len(points)-1):
#     segments += [i,i+1]
# tri = ComputeTriangularMesh(points, segments)
# print(tri.simplices)
def ComputeTriangularMesh(vertices, segments):
    from scipy.spatial import Delaunay
    from copy import deepcopy

    nVertices = len(vertices)
    tri = Delaunay(np.array(vertices))
    trigs = deepcopy(tri.simplices)
    
    #+++++++++++++++++++++++++++++++++
    #compute vertices2simplices list:
    vertices2simplices = [[]]*nVertices
    cnt = 0
    for trig in trigs:
        for i in trig:
            alist=list(vertices2simplices[i])
            alist.append(cnt)
            vertices2simplices[i] = alist    
        cnt += 1 #trig counter
        
    #print(trigs)
    #print(vertices2simplices)
    
    #+++++++++++++++++++++++++++++++++
    #compute neighbors:
    trigNeighbors = 0*trigs #-1 means no neighbor trig!
    trigNeighbors[:,:] = -1
    #run over all triangles
    for i in range(len(trigs)):
        for j in range(3):
            i0 = trigs[i,j]
            i1 = trigs[i,(j+1)%3]
            #actSeg = [i0, i1]
            listTest = vertices2simplices[i0] + vertices2simplices[i1]
            for trigIndex in listTest:
                if trigIndex < i:
                    for k in range(3):
                        t0 = trigs[trigIndex, k]
                        t1 = trigs[trigIndex, (k+1)%3]
                        if (i0 == t1) and (i1 == t0): #opposite trig orientation is reversed ...
                            trigNeighbors[i,j] = trigIndex
                            trigNeighbors[trigIndex,k] = i

    #print("neighbors=", trigNeighbors)                

    #+++++++++++++++++++++++++++++++++
    #compute inside triangles:
    trianglesInside = [-1]*len(trigs) #-1 is undefined, 0=outside, 1=inside
    
    for seg in segments: #triangles left to segment are inside
        listTest = vertices2simplices[seg[0]] + vertices2simplices[seg[1]]
        for trigIndex in listTest:
            for k in range(3):
                t0 = trigs[trigIndex, k]
                t1 = trigs[trigIndex, (k+1)%3]
                if (seg[0] == t0) and (seg[1] == t1): #inside triangle
                    trianglesInside[trigIndex] = 1
                elif (seg[0] == t1) and (seg[1] == t0): #outside triangle
                    trianglesInside[trigIndex] = 0
    #print(trianglesInside)

    #finally find remaining triangles (usually all triangles are on boundary, so nothing remains):
    undefinedTrigs = True
    while undefinedTrigs: #iterate as long as there are undefined triangles; usually only few iterations necessary
        undefinedTrigs = False
        #print("iterate neighbors")
        for i in range(len(trigs)):
            if trianglesInside[i] == -1: #still undefined
                found = False
                for j in range(3): #look at all neighbors
                    tn = trigNeighbors[i, j]
                    if trianglesInside[tn] != -1:
                        trianglesInside[i] = trianglesInside[tn]
                        found = True
                if not found:
                    undefinedTrigs = True

    #now create new list of interior triangles
    interiorTrigs = []
    for i in range(len(trigs)):
        if trianglesInside[i] == 1: 
            interiorTrigs += [list(trigs[i])]
    #print("interiorTrigs=",interiorTrigs)
    
    tri.simplices = np.array(interiorTrigs)
    
    return tri

#**function: convert point list into segments (indices to points); point indices start with pointIndexOffset
#**input:
#  invert: True: circle defines outter boundary; False: circle cuts out geometry inside a geometry
#  pointIndexOffset: point indices start with pointIndexOffset
#**output: return segments, containing list of lists of point indices for segments
def SegmentsFromPoints(points, pointIndexOffset = 0, invert=False, closeCurve=True):
    n = len(points)
    segments = np.zeros((n,2),dtype=int)
    if invert:
        for i in reversed(range(n-1)):
            segments[i,:] = [i+1, i]
    else:
        for i in range(n-1):
            segments[i,:] = [i, i+1]

    if closeCurve:
        if invert:
            segments[n-1,:] = [0, n-1] #close segments
        else:
            segments[n-1,:] = [n-1, 0] #close segments

    return segments

#**function: create points and segments, used in GraphicsDataSolidExtrusion(...) for circle with given parameters
#**input:
#  center: 2D center point (list/numpy array) for circle center
#  radius: radius of circle
#  invert: True: circle defines outter boundary; False: circle cuts out geometry inside a geometry
#  pointIndexOffset: point indices start with pointIndexOffset
#  nTiles: number of tiles/segments for circle creation (higher is finer)
#**output: return [points, segments], both containing lists of lists
#**notes: geometries may not intersect!
def CirclePointsAndSegments(center=[0,0], radius=0.1, invert = False, pointIndexOffset=0, nTiles=16):
    segments = np.zeros((nTiles,2),dtype=int)
    points = np.zeros((nTiles,2))
    
    if invert:
        myRange = reversed(range(nTiles))
    else:
        myRange = range(nTiles)
        
    for i in range(nTiles):
        phi = i/nTiles*2*pi
        points[i,:] = [radius*sin(phi)+center[0], radius*cos(phi)+center[1]]
        segments[i,:] = [(i+int(invert))%nTiles+pointIndexOffset, (i+1-int(invert))%nTiles+pointIndexOffset]

    segments = segments.tolist()
    points = points.tolist()
        
    return [points, segments]


#%%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#**function: create graphicsData for solid extrusion based on 2D points and segments; by default, the extrusion is performed in z-direction;
#            additional transformations are possible to translate and rotate the extruded body;
#**input:
#  vertices: list of pairs of coordinates of vertices in mesh [x,y], see ComputeTriangularMesh(...)
#  segments: list of segments, which are pairs of node numbers [i,j], defining the boundary of the mesh;
#            the ordering of the nodes is such that left triangle = inside, right triangle = outside; see ComputeTriangularMesh(...)
#  height:   height of extruded object
#  rot:      rotation matrix, which the extruded object point coordinates are multiplied with before adding offset
#  pOff:     3D offset vector added to extruded coordinates; the z-coordinate of the extrusion object obtains 0 for the base plane, z=height for the top plane
#  smoothNormals: if True, algorithm tries to smoothen normals at vertices and normals are added; creates more points; if False, triangle normals are used internally 
#  addEdges: if True or 1, edges at bottom/top are included in the GraphicsData dictionary; if 2, also mantle edges are included
#  edgeColor: optional color for edges
#  addFaces: if False, no faces are added (only edges)
#**output: graphicsData dictionary, to be used in visualization of EXUDYN objects
def GraphicsDataSolidExtrusion(vertices, segments, height, rot = np.diag([1,1,1]), pOff = [0,0,0], color = [0,0,0,1],
                               smoothNormals = False, addEdges = False, edgeColor=color4black, addFaces=True):
    n = len(vertices)
    n2 = n*2 #total number of vertices
    ns = len(segments)
    colors=[]
    for i in range(n2):
        colors+=color

    edges = []
    mantleEdges = (addEdges == 2)

    points = [[]]*n2
    for i in range(n):
        points[i] = [vertices[i][0],vertices[i][1],0]
    for i in range(n):
        points[i+n] = [vertices[i][0],vertices[i][1],height]

    if addEdges: #second set of points for top/bottom faces
        edges = [[]]*(ns*2)
        for cnt, seg in enumerate(segments):
            edges[cnt] = [seg[0], seg[1]]
            edges[cnt+ns] = [seg[0]+n, seg[1]+n]

    edges = list(np.array(edges).flatten())
    if smoothNormals: #second set of points for top/bottom faces
        #pointNormals = [[]]*(2*n2)
        for i in range(n2):
            colors+=color
        pointNormals = np.zeros((2*n2,3))

        #add normals from segments:
        for seg in segments:
            dirSeg = ebu.Normalize(np.array(vertices[seg[1]]) - np.array(vertices[seg[0]]))
            dirSeg3D = [dirSeg[1], -dirSeg[0], 0.] #this way points outwards ...
            pointNormals[seg[0]+2*n,:] += dirSeg3D
            pointNormals[seg[1]+2*n,:] += dirSeg3D
            pointNormals[seg[0]+3*n,:] += dirSeg3D
            pointNormals[seg[1]+3*n,:] += dirSeg3D
        
        for i in range(n2):
            lenSeg = ebu.NormL2(pointNormals[i,:])
            if lenSeg != 0.:
                pointNormals[i,:] = (1/lenSeg)*pointNormals[i,:]
            
        points2 = [[]]*n2
        for i in range(n):
            points2[i] = [vertices[i][0],vertices[i][1],0.]
            pointNormals[i+0*n,:] = [0.,0.,-1.]
            #pointNormals[i+2*n,:] = [0,0,-1]
        for i in range(n):
            points2[i+n] = [vertices[i][0],vertices[i][1],height]
            pointNormals[i+1*n,:] = [0.,0.,1.]
            #pointNormals[i+3*n,:] = [0,0,1]
        

    #transform points:
    pointsTransformed = []
    npRot = np.array(rot)
    npPoff = np.array(pOff)

    for i in range(n2):
        p = np.array(npRot @ points[i] + npPoff)
        pointsTransformed += list(p)
    
    if smoothNormals: #these are the points with normals from top/bottom surface
        for i in range(n2):
            p = np.array(npRot @ points2[i] + npPoff)
            pointsTransformed += list(p)

    #compute triangulation:
    tri = ComputeTriangularMesh(vertices, segments)
    trigs = tri.simplices
    nt =len(trigs)
    trigList = [[]] * (nt*2+ns*2) #top trigs, bottom trigs, circumference trigs (2 per quad)
    
    for i in range(nt):
        #print(list(trigs[i]))
        # trigList[i] = list(trigs[i])
        t = list(trigs[i])
        t.reverse()
        trigList[i] = copy.copy(t)
    for i in range(nt):
        t = list(trigs[i]+n)
        # t.reverse()
        trigList[i+nt] = copy.copy(t)
        
    #print("ns=",ns)
    #print("nt=",nt)
    off = n2*int(smoothNormals)
    for i in range(ns):
        trigList[2*nt+2*i  ] = [segments[i][0]+off,segments[i][1]+off,  segments[i][1]+n+off]
        trigList[2*nt+2*i+1] = [segments[i][0]+off,segments[i][1]+n+off,segments[i][0]+n+off]

        if mantleEdges:
            edges += [segments[i][0]+off,segments[i][0]+n+off]

    #print("trigList=",trigList)
    triangles = []
    if addFaces:
        for t in trigList:
            triangles += t
   
    data = {'type':'TriangleList', 'colors': colors, 'points':pointsTransformed, 'triangles':triangles}
    if addEdges:
        data['edgeColor'] = list(edgeColor)
        data['edges'] = edges

    if smoothNormals:
        data['normals'] = list(pointNormals.flatten())

    return data


