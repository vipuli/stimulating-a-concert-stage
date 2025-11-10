import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from StageLights import*
import csv
import os

#Initial setup
#plotting the image(Matplotlib   Plot Over an Image Background in Python, n.d.)
plt.rcParams["figure.figsize"] = [8, 6]
plt.rcParams["figure.autolayout"] = True

if os.path.exists("StageLight.jpg"):
    backdrop = plt.imread ("StageLight.jpg")
else : 
    backdrop = np.ones((500, 500, 3))

#plotting the axes and stage
fig, (ax0, ax1) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 10]}, figsize=(10, 10))
ax1.imshow(backdrop, extent=[0, 500, 0, 500])
ax1.set_aspect("equal")
ax0.set_aspect("equal")
ax0.fill([0, 500, 500, 0], [0, 0, 50, 50], color="silver")

ax1.set_xlim(0, 500)
ax1.set_ylim(0, 500)

#patching a triangular shape smoke machine
vertices = np.array([[5, 5], [15, 20], [20, 0]])
smokemachine = patches.Polygon(vertices, closed=True, fill=True, facecolor = "magenta")
ax1.add_patch(smokemachine)

#positioning bands
band_members = [
    {"position": (40, 280), "shape": "rectangle", "width": 8, "height": 45},
    {"position": (100, 300), "shape": "circle", "radius": 50},
    {"position": (150, 280), "shape": "rectangle", "width": 8, "height": 45},
    {"position": (345, 280), "shape": "rectangle", "width": 6, "height": 50},
    {"position": (400, 300), "shape": "circle", "radius": 50},
    {"position": (75, 350), "shape": "triangle", "side_length": 50},
    {"position": (445, 280), "shape": "rectangle", "width": 6, "height": 45},
    {"position": (200, 280), "shape": "triangle", "side_length": 75}
]

#plotting members of band
for member in band_members:
    position = member["position"]
    shape = member["shape"]

#plotting shapes and colors to the band
    if shape == "rectangle":
        width = member["width"]
        height = member["height"]
        rect = patches.Rectangle(position, width, height, edgecolor="yellow", facecolor="brown")
        ax1.add_patch(rect)
    elif shape == "circle":
        radius = member["radius"]
        circle = patches.Circle(position, radius, edgecolor="yellow", facecolor="silver")
        ax1.add_patch(circle)
    elif shape == "triangle":
        side_length = member["side_length"]
        #creating vertices of a triangle
        vertices = np.array([position, (position[0] + side_length, position[1]),
                             (position[0] + side_length / 2, position[1] + side_length)],
                            dtype=np.float32)
        triangle = patches.Polygon(vertices, closed=True, edgecolor="grey", facecolor="red")
        ax1.add_patch(triangle)
        
#plotting audience
audience_positions = [(40, 30), (80, 30), (118, 30), (152, 30), (200,20), (236, 30), (277, 30), (320, 30), (380, 26), (450, 28)] 


#positioning the audience
for position in audience_positions:
    ax1.add_patch(patches.Circle(position, 25, edgecolor="silver", facecolor="coral"))


#Fundamental circle that runs for a pre-defined number of cycles
num_frames = 60
sleep_time = 0.2
prop_step = 0
prop_direction = 2
colors =['pink', 'blue', 'yellow']

# Try to load choreography CSV
choreo_data = []
if os.path.exists("choreography.csv"):
    with open("choreography.csv") as f:
        reader = csv.DictReader(f)
        choreo_data = list(reader)

for v in range(num_frames):
    lights = []
    smokes = []
    prop_obj = []

    # Use choreography if available
    if v < len(choreo_data):
        row = choreo_data[v]
        light_color = row.get("light_color", random.choice(colors))
        smoke_intensity = float(row.get("smoke_intensity", 0.5))
    else:
        light_color = random.choice(colors)
        smoke_intensity = random.uniform(0.3, 0.6)

    #stimulating Lights
    for l in range(5): #to plot 5 light beams
        a = list(range(50, 500, 100)) #lights of x coordinate
        b = [25, 25, 25, 25, 25] # lights of y coordinate
        x = a[l]
        y = b[l]
        inten=random.randint(0, 10) / 10
        light = Lights((x, y), light_color, inten)
        lights.append(light)


    # Smoke diffusion
    for _ in range(10):
        x = random.randint(0, 500)
        y = random.randint(0, 200)
        smoke = SmokeMachine((x, y), smoke_intensity)
        smoke.diffuse()
        smokes.append(smoke)

    prop_step += 10 * prop_direction
    if prop_step>= 380:
        prop_direction= -2
    elif prop_step<= 0:
        prop_direction= 2

    prop = Props(prop_step, random.choice(colors))
    prop_obj.append(prop)


    #Plotting Lights and Beams
    for light in lights:
        light.plotLight(ax0)
        light.plotBeam(ax1)

    #Plotting smoke
    for smoke in smokes:
        smoke.plotSmoke(ax1)

    for propss in prop_obj:
        propss.jukeBox(ax1)
    
    plt.pause(sleep_time)


    # Cleanup
    for light in lights:
        light.removeBeam()
    for smoke in smokes:
        smoke.removeSmoke()
    for prop in prop_obj:
        for p in prop.getProp():
            p.remove()
    

plt.show()
