import matplotlib.pyplot as plt
import random
import numpy as np
import matplotlib.patches as patches


#according to practest3 making light class
class Lights():
    
    def __init__(self,pos,color,intensity):
        self.pos=pos
        self.color=color
        self.intensity=intensity

    #plot lights
    def plotLight(self, ax):
        radius = 20
        self.light = plt.Circle(self.pos, radius, color=self.color, alpha=self.intensity,zorder=3)
        ax.add_patch(self.light)

    #plot light beams    
    def plotBeam(self, ax):
        a = [490, 490, 500, 500]
        b = [490, 490, 0, 0]
        c = self.pos[0] - 20
        l = [c, c + 40, c + 40, c]
        self.top_bar = ax.fill(l, a, color=self.color, alpha=self.intensity, zorder=3)
        self.beam = ax.fill(l, b, color=self.color, alpha=self.intensity, zorder=3)

    def removeBeam(self):
        for patch in self.top_bar:
            patch.remove()
        for patch in self.beam:
            patch.remove()
        self.light.remove()    

#making smokes according to practest3
class SmokeMachine():

    def __init__(self, pos,intensity,color = "lightblue"):
        self.pos = pos
        self.intensity=intensity
        self.color = color
        self.radius = 20

    def plotSmoke(self, ax):
        self.circle=plt.Circle(self.pos, radius=self.radius, color=self.color,alpha=self.intensity,zorder=3)
        ax.add_patch(self.circle)
        
    def diffuse(self):
        dx = random.randint(-5, 5)
        dy = random.randint(5, 10)
        new_x = max(0, min(500, self.pos[0] + dx))
        new_y = max(0, min(500, self.pos[1] + dy))
        self.pos = (new_x, new_y)
        self.intensity = max(0.1, self.intensity - 0.02)  # fade slowly
 
    def removeSmoke(self):
        """Remove smoke patch after each frame."""
        self.circle.remove()


#making the props
class Props():
    def __init__(self,pos,color):
        self.pos = pos
        self.color = color
        
    def jukeBox(self,ax):#(GeeksforGeeks, 2020)
        i=self.pos
        self.q=patches.Rectangle((i,0), 100,40,color='purple')
        self.r=plt.Circle(((i+20),60),20,color=self.color)
        self.s=plt.Circle(((i+80),60),20,color=self.color)
        self.t=plt.Circle(((i+80),60),10,color='grey')
        self.u=plt.Circle(((i+20),60),10,color='grey')
        ax.add_patch(self.q)
        ax.add_patch(self.r)
        ax.add_patch(self.s)
        ax.add_patch(self.t)
        ax.add_patch(self.u)

    def getProp(self):
        return [self.q, self.r, self.s, self.t, self.u]

