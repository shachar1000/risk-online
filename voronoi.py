from __future__ import division
import collections
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, KDTree, Voronoi, voronoi_plot_2d
from perlin import perlinClass
from voronoi_close import voronoi_finite_polygons_2d
import random
from collections import Counter
import io
import base64
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from noiseEdge import noiseEdgeWrapper
from decimal import *



def voronoiPolygons(P, delauny=True):
    if delauny==True:
        delauny = Delaunay(P)
        triangles = delauny.points[delauny.vertices]
        circum_centers = np.array([triangle_csc(tri) for tri in triangles])
        vor = Voronoi(circum_centers)
    else:
        vor = Voronoi(P)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    polygons = []
    for reg in regions:
        polygon = vertices[reg] #dict
        polygons.append(polygon)
    return polygons

def improveVoronoi(polys):
    data = centroids(polys)
    return voronoiPolygons(data,delauny=False)

def random_color(str=True, alpha=0.5):
    rgb = [random.randint(0, 255) for i in range(3)]
    if str:
        return "rgba"+str(tuple(rgb+[alpha]))
    else:
        return list(np.array(rgb)/255) + [alpha]

def triangle_csc(pts):
    # diffs = x2-x1 and y2-y1 for 2 vertices of the triangle
    diffs = np.diff(pts[:3], axis=0) # the :3 is because we want only 2 vertices and not 3 for the calculations
    slopes = [(diffs[i][1]/diffs[i][0]) for i in range(2)]
    means = [[(pts[i][0]+pts[i+1][0])/2, (pts[i][1]+pts[i+1][1])/2] for i in range(2)]
    slopesOfPerpendicularBisectors = [(-1)/slopes[i] for i in range(len(slopes))]
    #y=mx+b   =>    b=y-mx
    b = [means[i][1]-(slopesOfPerpendicularBisectors[i]*means[i][0]) for i in range(2)]
    # m1x+b=m2x+b
    x = ((b[1]-b[0])/(slopesOfPerpendicularBisectors[0]-slopesOfPerpendicularBisectors[1]))
    y = (x*slopesOfPerpendicularBisectors[0])+b[0]
    return (x, y)

def displayVoronoi(polys, random=True, players=None):
    axes = plt.subplot(1,1,1)
    plt.axis([-0, 1, -0, 1])
    if players:
        playersUnique = list(set(players)) # set returns unique elements
        colors = [random_color(str=False, alpha=1) for i in range(len(playersUnique))]
        #color for every player (and ocean)
    for count, poly in enumerate(polys):
        if random:
            p = matplotlib.patches.Polygon(poly, facecolor=random_color(str=False, alpha=1))
        else:
            polyPlayer = players[count] #the player of the poly is the index of poly in the players array
            indexOfColor = playersUnique.index(polyPlayer)
            color = colors[indexOfColor]
            p = matplotlib.patches.Polygon(poly, facecolor=color)
        axes.add_patch(p)

    def fig_to_base64():
        img = io.BytesIO()
        plt.savefig(img, format='png',
                    bbox_inches='tight')
        img.seek(0)
        return base64.b64encode(img.getvalue())

    encoded = fig_to_base64()
    return '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

def centroids(polys):
    # n sides of all polygons
    lengths = [polys[i].shape[0] for i in range(len(polys))]
    sumX = [np.sum([polys[i][:, 0]]) for i in range(len(polys))]
    sumY = [np.sum([polys[i][:, 1]]) for i in range(len(polys))]
    centroids = [(sumX[i]/lengths[i], sumY[i]/lengths[i]) for i  in range(len(polys))]
    return centroids

def adjacent(list, n):
    groups = [list[i:i + n] for i in range(len(list) + 1 - n)]
    groups.append([list[0], list[::-1][0]])
    return groups

#noiseEdge([[3, 3], [3, 0]], [[0, 1.5], [6, 1.5]])

if __name__ == '__main__':
    # triangle = [
    # [3, 1],
    # [-1, 3],
    # [-3, -3]
    # ]
    # print(triangle_csc(triangle))
    P = np.random.random((200,2))
    polys = voronoiPolygons(P)
    for i in range(10):
        polys = improveVoronoi(polys)

    # point = Point(0.2, 0.2)
    # plt.scatter([point.x], [point.y], marker='.', zorder=2)
    # for count, poly in enumerate(polys):
    #     if Polygon(poly).contains(point):
    #         polys.pop(count)

    data = centroids(polys)
    displayVoronoi(polys)

    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]

    plt.scatter(x_val, y_val, marker='.', zorder=2)

    print(polys[45])

    def compare(a, b):
        return [i for i in range(len(a)) if a[i] in b]

    print(compare([[3, 3],[4, 4]],[[4, 4],[5, 5], [3, 3]]))

    def removeDecimals(points, num):
        return [[float(str(coor)[1:str(coor).index('.')+num+1]) for coor in point] for point in points]



    print(polys)
    for count, poly in enumerate(polys):
        commonVerticesIndexes = compare(polys[45], poly)
        commonVertices = [polys[45][commonVerticesIndexes[i]] for i in range(len(commonVerticesIndexes))]
        centroids = [data[count], data[45]]
        if len(commonVertices) == 2:
            newDots = noiseEdgeWrapper(commonVertices, centroids, 0)

            polyList = [list(x) for x in poly] # convert numpy matrix to list
            polyList = [[coor for coor in point] for point in polyList ]
            #polyList = removeDecimals(polyList, 4)

            indexPoly = polyList.index(commonVertices[0])
            indexPoly45 = polys[45].index(commonVertices[0])
            # print(indexPoly1)
            # print(indexPoly2)
            print("  ")
            print("  ")
    #print(removeDecimals([[1.36436284637, 4.373692749374937],[3.87473846, 4.4236472838234]], 5))

    #X,Y = P[:,0],P[:,1]
    #plt.scatter(X, Y, marker='.', zorder=2)

    plt.show()
