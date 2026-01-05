from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
import uuid
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



def generateMap(height, width, seed, scale, octaves, bias, persistance, lacunarity, name):
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

           
            distX = abs(width / 2 - x)
            distY = abs(height / 2 - y)
            dist = max(distX, distY)
            maxWidth = width / 2 - bias
            delta = dist / maxWidth
            gradient = delta ** 2
            heightMap[y][x] *= max(0.0, 1.0 - gradient)


            

        os.system("cls")
        print("Generating Map...\n(" + str(height) + "px X " + str(width) + "px)\n--" + str(int(y/height*100))+"%--")
      
    os.system("cls")
    print("Generating Map...\n(" + str(height) + "px X " + str(width) + "px)\n--Done!--")
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

def init(WIDTH = 256, HEIGHT = 256, SEED = uuid.uuid1().int >> 64, BIAS = 10, OCTAVES = 1, PERSISTANCE = 0.5, LACUNARITY = 2):
  SCALE = max(WIDTH, HEIGHT) / 4
  generateMap(HEIGHT, WIDTH, SEED, SCALE, OCTAVES, BIAS, PERSISTANCE, LACUNARITY, "MapSeed" + str(SEED))

if __name__ == "__main__":
    init(OCTAVES = 5)