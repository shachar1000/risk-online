import numpy as np
import matplotlib.pyplot as plt


class perlinClass():
    def __init__(self, x, y):
        self.perlinGrid = self.perlin(x, y)
        self.perlinGrid = self.partition(3, self.perlinGrid)

    def perlin(self, x, y, seed=1):
        # permutation table
        np.random.seed(seed)
        p = np.arange(256,dtype=int)
        np.random.shuffle(p)
        p = np.stack([p,p]).flatten()
        # print(p[:256])
        # print("########")
        # print(p[256:512])

        xi = x.astype(int)
        yi = y.astype(int)
        xf = x - xi
        yf = y - yi
        u = fade(xf)
        v = fade(yf)
        n00 = gradient(p[p[xi]+yi],xf,yf)
        n01 = gradient(p[p[xi]+yi+1],xf,yf-1)
        n11 = gradient(p[p[xi+1]+yi+1],xf-1,yf-1)
        n10 = gradient(p[p[xi+1]+yi],xf-1,yf)
        x1 = lerp(n00,n10,u)
        x2 = lerp(n10,n11,u)
        return lerp(x2,x1,v)

    def partition(self, numPlayers, perlinGrid):
        minX = min(perlinGrid.flatten())
        maxX = max(perlinGrid.flatten())
        numPlayers = 3
        rangeVector = [[minX+((maxX-minX)/numPlayers)*(n), minX+(((maxX-minX)/numPlayers)*(n+1))] for n in range(numPlayers)]
        print(rangeVector)
        for y in range(len(perlinGrid)):
            for x in range(len(perlinGrid[0])):
                pixel = perlinGrid[y][x]
                for i in range(3):
                    if ((rangeVector[i][0] <= pixel) and (pixel <= rangeVector[i][1])):
                        perlinGrid[y][x] = rangeVector[i][0]
        return perlinGrid

def lerp(a,b,x):
    "linear interpolation"
    return a + x * (b-a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h,x,y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0,1],[0,-1],[1,0],[-1,0]])
    g = vectors[h%4]
    return g[:,:,0] * x + g[:,:,1] * y

if __name__ == '__main__':
    lin = np.linspace(0,2,10,endpoint=False)
    #10 spaces between 0 and 1
    y,x = np.meshgrid(lin,lin)
    perlinGrid = perlinClass(x,y)

    plt.imshow(perlinGrid.perlinGrid)
    plt.show()
