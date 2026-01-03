# personal notes
# set 0 < R < 1, N > 2 for more interesting patterns.
# An interesting case happens when we let r = np.sqrt(2).
# When R = 2, it generates some very abstract pattern.
# to see the slope of eps vs boxes comment 66-71 and uncomment 84-89.
# the value of P and the number eps is multiplied by in line 77 may need to be adjusted to get the program to work.
# please note that if P is decreased or the number in line 77 is increased then you will get a worse aproximation of dimension.
# the number in line 77 should be in the range 1>n>0.

# imports
import numpy as np
import math
import matplotlib.pyplot as plt
import random

N=3      # starting vertices
R=2     # contraction value
P=150000 # number of point

# variables needed later for box counting
eps=0.1
epslogvalues=[]
Nlogvalues=[]

# list of x coordinates with corresponding y coordinates for points
xs, ys = [], []

# main functions
def chaos_game_polygon(n_vertices,r,n_points):
    # starting point
    x, y = 0.0, 0.0
    # create regular polygon vertices on unit circle
    angles = np.linspace(0, 2*np.pi, n_vertices, endpoint=False)
    vertices = [(np.cos(a), np.sin(a)) for a in angles]
    # creates new vertices equal to n_points
    for i in range(n_points):
        vx, vy = random.choice(vertices)
        x = x + r*(vx - x)
        y = y + r*(vy - y)
        xs.append(x)
        ys.append(y)

def n_of_boxes(epsilon):
    # Determine the bounding box needed to 
    min_x, min_y = min(xs), min(ys)
    max_x, max_y = max(xs), max(ys)
    width = max_x - min_x
    height = max_y - min_y
    # creates sub-boxes of the bounding box
    cols=math.ceil(width/epsilon)+1
    rows=math.ceil(height/epsilon)+1
    boxes=np.zeros((rows,cols), dtype=np.int8)
    # make boxes[i,j] = 1 if contains a point of the orbit
    for n in range(0, len(xs)):
        # coordinates of the box where the point belongs
        cc=math.floor((xs[n]-min_x)/epsilon)
        rc=math.floor((ys[n]-min_y)/epsilon)
        if boxes[rc,cc]==0:
            boxes[rc,cc]=1
    return (np.sum(boxes))

# makes shape
chaos_game_polygon(N,R,P)

# plot
plt.figure(figsize=(6,6))
plt.scatter(xs, ys, s=0.2,color='black')
plt.gca().set_aspect('equal')
plt.title(f"Chaos Game: {N}-gon, r={R}, points={P}")
plt.axis('off')
plt.show()

for i in range(0,10):
    epslogvalues.append(np.log(eps))
    count=n_of_boxes(eps)
    Nlogvalues.append(np.log(count))
    eps=0.75*eps

# fits the plot (eps values vs number of boxes) to a linear graph    
coefficients = np.polyfit(epslogvalues[:-2],Nlogvalues[:-2], 1)   
x_fit = np.linspace(np.min(epslogvalues), np.max(epslogvalues), 500)
y_fit = np.polyval(coefficients, x_fit)

#plt.plot(epslogvalues,Nlogvalues,'o',   color='blue')
#plt.plot(x_fit,y_fit,'-',   color='green')
#plt.xlabel('ln(epsilon)')
#plt.ylabel('ln(n-boxes)')
#plt.grid()
#plt.show()

print("dimensions=", abs(coefficients[0]))