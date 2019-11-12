from __future__ import division
import collections
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay, KDTree, Voronoi, voronoi_plot_2d
from perlin import perlinClass
from voronoi_close import voronoi_finite_polygons_2d
import random
# an adaptation of https://stackoverflow.com/a/15783581/60982
# using ideas from https://stackoverflow.com/a/9471601/60982

def voronoiPolygons(P):
    delauny = Delaunay(P)
    triangles = delauny.points[delauny.vertices]

    circum_centers = np.array([triangle_csc(tri) for tri in triangles])
    print(circum_centers)
    vor = Voronoi(circum_centers)
    regions, vertices = voronoi_finite_polygons_2d(vor)
    polygons = []
    for reg in regions:
        polygon = vertices[reg] #dict
        polygons.append(polygon)
    return polygons

def random_color(str=True, alpha=0.5):
    rgb = [random.randint(0, 255) for i in range(3)]
    if str:
        return "rgba"+str(tuple(rgb+[alpha]))
    else:
        return list(np.array(rgb)/255) + [alpha]

def triangle_csc(pts):

    # diffs = x2-x1 and y2-y1 for 2 vertices of the triangle
    diffs = np.diff(pts[:3], axis=0) # the :3 is because we want only 2 vertices and not 3 for the calculations
    print(diffs)
    print(pts[:3])
    print("")

    slopes = [(diffs[i][1]/diffs[i][0]) for i in range(2)]
    means = [[(pts[i][0]+pts[i+1][0])/2, (pts[i][1]+pts[i+1][1])/2] for i in range(2)]
    print("lol")
    print(slopes)
    print("lol")
    print(means)
    print("lol")
    slopesOfPerpendicularBisectors = [(-1)/slopes[i] for i in range(len(slopes))]
    print(slopesOfPerpendicularBisectors)
    print("lol")
    #y=mx+b   =>    b=y-mx
    b = [means[i][1]-(slopesOfPerpendicularBisectors[i]*means[i][0]) for i in range(2)]
    # m1x+b=m2x+b
    x = ((b[1]-b[0])/(slopesOfPerpendicularBisectors[0]-slopesOfPerpendicularBisectors[1]))
    y = (x*slopesOfPerpendicularBisectors[0])+b[0]
    print(b)

    return (x, y)

if __name__ == '__main__':
    triangle = [
    [3, 1],
    [-1, 3],
    [-3, -3]
    ]
    print(triangle_csc(triangle))
    P = np.random.random((200,2))

    fig = plt.figure(figsize=(4.5,4.5))
    axes = plt.subplot(1,1,1)

    plt.axis([-0.05,1.05,-0.05,1.05])

    polys = voronoiPolygons(P)

    for poly in polys:
        p = matplotlib.patches.Polygon(poly, facecolor=random_color(str=False, alpha=1))
        axes.add_patch(p)

    print(polys[0])
    length = polys[0].shape[0]
    sumX = np.sum(polys[0][:, 0])
    sumY = np.sum(polys[0][:, 1])
    centroid = (sumX/length, sumY/length)
    print(centroid)
    plt.scatter(centroid[0],centroid[1],marker="h")

    X,Y = P[:,0],P[:,1]

    #plt.scatter(X, Y, marker='.', zorder=2)
    plt.scatter(centroid[0],centroid[1],marker="h")
    plt.scatter(centroid[0],centroid[1])
    print(centroid[0])

    plt.axis([-0.05,1.05,-0.05,1.05])
    plt.show()
