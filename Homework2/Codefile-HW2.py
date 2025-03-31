import numpy as np
import matplotlib.pyplot as plt

print("HW-2: Drawing a line with co-ordinate system")
pts=np.zeros((2,2))
for i in range(2):
    for j in range(2):
        if j==0:
            pts[i,j]=input("Enter the x-coordinate for point"+str(i)+": ")
        else:
            pts[i,j]=input("Enter the y-coordinate for point"+str(i)+": ")
#print("The two points are: "+ str(pts))
for i in range(1):
    print(pts[i])
    print(pts[i+1])
    if pts[i][0]!=pts[i+1][0] and pts[i][1]!=pts[i+1][1]:
        m=(pts[i+1][1]-pts[i][1])/(pts[i+1][0]-pts[i][0])
        b=(pts[i+1][1])-(m*pts[i+1][0])
        x_main = np.linspace(pts[i][0],pts[i+1][0])
        y_main=(m*x_main)+b
        plt.plot(x_main,y_main)
        plt.show()
    else:
        print("Cannot divide by zero")
