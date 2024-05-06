from __future__ import division
# 这是一个关于私人用途的代码原文件库
import numpy as np
from numpy import *
import sys  # maxint

# C-均值聚类
def FCM_train(X,n_centers,m,max_iter = 100,theta=1e-5,seed=0):
    rng = np.random.RandomState(seed)
    N,D = np.shape(X)
    # 随机初始化关系矩阵
    U = rng.uniform(size=(N, n_centers))
    # 保证每行和为1
    U = U/np.sum(U,axis=1,keepdims=True)
    # 开始迭代
    for i in range(max_iter):
        print(i)
        U_old = U.copy()
        centers = FCM_getCenters(U,X,m)
        U=FCM_getU(X,centers,m)
        # 两次关系的距离矩阵过小，结束训练
        if np.linalg.norm(U-U_old) < theta:
            break
    return centers,U

def FCM_getCenters(U,X,m):
    N,D = np.shape(X)
    N,C = np.shape(U)
    um = U** m
    tile_X = np.tile(np.expand_dims(X,1),[1,C,1])
    tile_um = np.tile(np.expand_dims(um,1),[1,1,D])
    temp = tile_X*tile_um
    new_C = np.sum(temp,axis=0)/np.expand_dims(np.sum(um,axis=0),axis=-1)
    return new_C

def FCM_getU(X,Centers,m):
    N,D =np.shape(X)
    C,D = np.shape(Centers)
    temp = FCM_dist(X,Centers)**float(2/(m-1))
    tile_temp = np.tile(np.expand_dims(temp,1),[1,C,1])
    denominator_ = np.expand_dims(temp,-1)/tile_temp
    return 1/np.sum(denominator_,axis=-1)

def qhull2D(sample):
    link = lambda a, b: concatenate((a, b[1:]))
    edge = lambda a, b: concatenate(([a], [b]))
    def dome(sample, base):
        h, t = base
        dists = dot(sample - h, dot(((0, -1), (1, 0)), (t - h)))
        outer = repeat(sample, dists > 0, 0)
        if len(outer):
            pivot = sample[argmax(dists)]
            return link(dome(outer, edge(h, pivot)),
                        dome(outer, edge(pivot, t)))
        else:
            return base

    if len(sample) > 2:
        axis = sample[:, 0]
        base = take(sample, [argmin(axis), argmax(axis)], 0)
        return link(dome(sample, base), dome(sample, base[::-1]))
    else:
        return sample

def minBoundingRect(hull_points_2d):
    #print "Input convex hull points: "
    #print hull_points_2d

    # Compute edges (x2-x1,y2-y1)
    edges = zeros( (len(hull_points_2d)-1,2) ) # empty 2 column array
    for i in range( len(edges) ):
        edge_x = hull_points_2d[i+1,0] - hull_points_2d[i,0]
        edge_y = hull_points_2d[i+1,1] - hull_points_2d[i,1]
        edges[i] = [edge_x,edge_y]
    #print "Edges: \n", edges

    # Calculate edge angles   atan2(y/x)
    edge_angles = zeros( (len(edges)) ) # empty 1 column array
    for i in range( len(edge_angles) ):
        edge_angles[i] = math.atan2( edges[i,1], edges[i,0] )
    #print "Edge angles: \n", edge_angles

    # Check for angles in 1st quadrant
    for i in range( len(edge_angles) ):
        edge_angles[i] = abs( edge_angles[i] % (math.pi/2) ) # want strictly positive answers
    #print "Edge angles in 1st Quadrant: \n", edge_angles

    # Remove duplicate angles
    edge_angles = unique(edge_angles)
    #print "Unique edge angles: \n", edge_angles

    # Test each angle to find bounding box with smallest area
    min_bbox = (0, sys.maxsize, 0, 0, 0, 0, 0, 0) # rot_angle, area, width, height, min_x, max_x, min_y, max_y  sys.maxint
    print ("Testing", len(edge_angles), "possible rotations for bounding box... \n")
    for i in range( len(edge_angles) ):

        # Create rotation matrix to shift points to baseline
        # R = [ cos(theta)      , cos(theta-PI/2)
        #       cos(theta+PI/2) , cos(theta)     ]
        R = array([ [ math.cos(edge_angles[i]), math.cos(edge_angles[i]-(math.pi/2)) ], [ math.cos(edge_angles[i]+(math.pi/2)), math.cos(edge_angles[i]) ] ])
        #print "Rotation matrix for ", edge_angles[i], " is \n", R

        # Apply this rotation to convex hull points
        rot_points = dot(R, transpose(hull_points_2d) ) # 2x2 * 2xn
        #print "Rotated hull points are \n", rot_points

        # Find min/max x,y points
        min_x = nanmin(rot_points[0], axis=0)
        max_x = nanmax(rot_points[0], axis=0)
        min_y = nanmin(rot_points[1], axis=0)
        max_y = nanmax(rot_points[1], axis=0)
        #print "Min x:", min_x, " Max x: ", max_x, "   Min y:", min_y, " Max y: ", max_y

        # Calculate height/width/area of this bounding rectangle
        width = max_x - min_x
        height = max_y - min_y
        area = width*height
        #print "Potential bounding box ", i, ":  width: ", width, " height: ", height, "  area: ", area

        # Store the smallest rect found first (a simple convex hull might have 2 answers with same area)
        if (area < min_bbox[1]):
            min_bbox = ( edge_angles[i], area, width, height, min_x, max_x, min_y, max_y )
        # Bypass, return the last found rect
        #min_bbox = ( edge_angles[i], area, width, height, min_x, max_x, min_y, max_y )

    # Re-create rotation matrix for smallest rect
    angle = min_bbox[0]
    R = array([ [ math.cos(angle), math.cos(angle-(math.pi/2)) ], [ math.cos(angle+(math.pi/2)), math.cos(angle) ] ])
    #print "Projection matrix: \n", R

    # Project convex hull points onto rotated frame
    proj_points = dot(R, transpose(hull_points_2d) ) # 2x2 * 2xn
    #print "Project hull points are \n", proj_points

    # min/max x,y points are against baseline
    min_x = min_bbox[4]
    max_x = min_bbox[5]
    min_y = min_bbox[6]
    max_y = min_bbox[7]
    #print "Min x:", min_x, " Max x: ", max_x, "   Min y:", min_y, " Max y: ", max_y

    # Calculate center point and project onto rotated frame
    center_x = (min_x + max_x)/2
    center_y = (min_y + max_y)/2
    center_point = dot( [ center_x, center_y ], R )
    #print "Bounding box center point: \n", center_point

    # Calculate corner points and project onto rotated frame
    corner_points = zeros( (4,2) ) # empty 2 column array
    corner_points[0] = dot( [ max_x, min_y ], R )
    corner_points[1] = dot( [ min_x, min_y ], R )
    corner_points[2] = dot( [ min_x, max_y ], R )
    corner_points[3] = dot( [ max_x, max_y ], R )
    #print "Bounding box corner points: \n", corner_points

    #print "Angle of rotation: ", angle, "rad  ", angle * (180/math.pi), "deg"

    return (angle, min_bbox[1], min_bbox[2], min_bbox[3], center_point, corner_points) # rot_angle, area, width, height, center_point, corner_points

def Get_MBR(points):
    '求平面包围盒'
    hull_points = qhull2D(points)  # Find convex hull 查找凸包
    hull_points = hull_points[::-1]  # Reverse order of points, to match output from other qhull implementations 颠倒点的顺序，以匹配其他qhull实现的输出
    print('凸包点: \n', hull_points, "\n")
    (rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)  # Find minimum area bounding rectangle 查找最小面积边界矩形
    print ("Minimum area bounding box 最小面积边界框:")
    print ("Rotation angle 旋转角:", rot_angle, "rad  (", rot_angle*(180/math.pi), "deg )")
    print ("Width 宽度:", width, " Height 长度:", height, "  Area 面积:", area)
    print ("Center point 中心点: \n", center_point) # numpy array
    print ("Corner points 转角点: \n", corner_points, "\n")  # numpy array
    RectangleProperties = np.array([width,height,area])  # 合并矩形属性
    return corner_points,RectangleProperties

def Get_KB(x1, y1, x2, y2):
    '通过两点式求二维直线的截距和斜率'
    # 计算斜率
    slope = (y2 - y1) / (x2 - x1)
    # 计算截距
    intercept = y1 - slope * x1
    print(f"斜率：{slope}")
    print(f"截距：{intercept}")
    return slope, intercept