import random
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
new = []


def random_color(str=True, alpha=0.5):
    rgb = [random.randint(0, 255) for i in range(3)]
    if str:
        return "rgba"+str(tuple(rgb+[alpha]))
    else:
        return list(np.array(rgb)/255) + [alpha]

def adjacent(list, n):
    groups = [list[i:i + n] for i in range(len(list) + 1 - n)]
    groups.append([list[0], list[::-1][0]])
    return groups

def noiseEdge(polys, centroids, count):
    polygon = [polys[0], centroids[0], polys[1], centroids[1]]
    sides = adjacent(polygon, 2)
    means = [[(sides[y][x][coor]+sides[y][x+1][coor])/2 for coor in range(2)] for y in range(len(sides)) for x in range(len(sides[y])-1)]
    # means = []
    # for i in range(len(sides)): # which side
    #     means.append([])
    #     for y in range(len(sides[i])-1): # which point
    #         for coor in range(len(sides[i][y])): # which
    #             means[i].append((sides[i][y][coor]+sides[i][y+1][coor])/2)
    randomPoint = [random.uniform(centroids[0][coor], centroids[1][coor]) for coor in range(2)]
    print(count)
    print("randomPoint")
    print(randomPoint)
    #newCentroids = [means[(i-1)*2:i*2] for i in range(1, 3)] # array of 2 arrays of polys for each new polygon
    newCentroids = [[means[0], means[3]],means[1:3]]
    newPolys = [[randomPoint, polys[0]],[randomPoint, polys[1]]]
    print("newPolys")
    print(newPolys)
    print("newCentroids")
    print(newCentroids)
    print("  ")
    if (count == 6):
        new.append(newPolys)
    if count < 7:
        count = count + 1
        noiseEdge(newPolys[0], newCentroids[0], count)
        noiseEdge(newPolys[1], newCentroids[1], count)



noiseEdge([[3, 3], [3, 0]], [[0, 1.5], [6, 1.5]], 0)





poly = [[3, 3],[6, 1.5],[3, 0],[0, 1.5]]
axes = plt.subplot(1,1,1)
plt.axis([-0, 10, -0, 10])
p = matplotlib.patches.Polygon(poly, facecolor=random_color(str=False, alpha=1))
axes.add_patch(p)

linePairs = [line for pair in new for line in pair]
newDots = [dot for line in linePairs for dot in line]

new_k = []
for elem in newDots:
    if elem not in new_k:
        new_k.append(elem)
newDots = new_k

newDots = sorted(newDots , key=lambda k: [k[1], k[0]]) # sort by y

for i in range(len(newDots)-1):
    plt.plot([newDots[i][0], newDots[i+1][0]], [newDots[i][1], newDots[i+1][1]], 'k-', lw=0.6)

print(newDots)

x = [dot[0] for dot in newDots]
y = [dot[1] for dot in newDots]

#plt.scatter(x, y, zorder=10)
plt.show()
