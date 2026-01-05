from opensimplex import OpenSimplex 
import numpy as np 
from PIL import Image
import uuid
import math
import os


COLORS = {
  "DEEPWATER" : (0, 62, 178),
  "WATER" : (9, 82, 198),
  "SHORE" : (20, 100, 210),
  "SAND" : (254, 224, 179),
  "GRASS" : (9, 120, 93),
  "DARKGRASS" : (10, 107, 72),
  "DARKESTGRASS" : (11, 94, 51),
  "DARKROCKS" : (140, 142, 123),
  "ROCKS" : (160, 162, 143),
  "SNOW" : (255, 255, 255)
}


def getColor(heightVal):
    if heightVal < 0:
        heightVal = 0
    if heightVal > 255:
        heightVal = 255

    if heightVal <= 84:
        return COLORS["DEEPWATER"]
    elif heightVal <= 98:
        return COLORS["WATER"]
    elif heightVal <= 110:
        return COLORS["SHORE"]
    elif heightVal <= 115:
        return COLORS["SAND"]
    elif heightVal <= 134:
        return COLORS["GRASS"]
    elif heightVal <= 164:
        return COLORS["DARKGRASS"]
    elif heightVal <= 200:
        return COLORS["DARKESTGRASS"]
    elif heightVal <= 224:
        return COLORS["DARKROCKS"]
    elif heightVal <= 242:
        return COLORS["ROCKS"]
    elif heightVal <= 255:
        return COLORS["SNOW"]
    return COLORS["DEEPWATER"]



def generateMap(width = 256, height = 256, seed = uuid.uuid1().int >> 64, bias = 10, octaves = 11, persistance = 0.5, lacunarity = 2):
    
    scale = max(width, height) / 4
    heightMap = np.empty((height, width), dtype=np.short)
    noise = OpenSimplex(seed=seed)
    
    for y in range(0, height):
        for x in range(0, width):
            amplitude = 1
            frequency = 1
            noiseHeight = 0

            for octave in range(0, octaves):
                sampleX = x / scale * frequency
                sampleY = y / scale * frequency

                value = noise.noise2(sampleX, sampleY)
                noiseHeight += value * amplitude

                amplitude *= persistance
                frequency *= lacunarity
                heightMap[y][x] = (noiseHeight + 1) * 128
            
            x_falloff = -((x-(width/2))**2)/(4**((math.log(width)/math.log(2))-1)) + 1
            y_falloff = -((y-(height/2))**2)/(4**((math.log(height)/math.log(2))-1)) + 1
            heightMap[y][x] *= (x_falloff + y_falloff)/2

        os.system("cls")
        print("Generating Map...\n(" + str(width) + "px X " + str(height) + "px)\n--" + str(int(y/height*100))+"%--")
      
    os.system("cls")
    print("Generating Map...\n(" + str(width) + "px X " + str(height) + "px)\n--Done!--")


    colourMap = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(0, height):
        for x in range(0, width):
            colourMap[y][x] = getColor(heightMap[y][x])

    image = Image.fromarray(colourMap, 'RGB')
    
    current_dir = os.path.dirname(os.path.abspath(__file__))

    try:
        lastfilename = os.listdir(current_dir + "/maps")[-1]
        newindex = int(lastfilename[3:-4]) + 1
    except:
      newindex = 0
    
    image.save(current_dir + "/maps/Map" + str(newindex) + ".png")
    return image


  

if __name__ == "__main__":
  iterations = int(input("Please Enter Number Of Run Iterations:  "))
  for i in range(0, iterations):
    generateMap(width = 256,  height = 256, seed = uuid.uuid1().int >> 64, bias = 10, octaves = 11, persistance = 0.5, lacunarity = 2)