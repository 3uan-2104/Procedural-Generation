from opensimplex import OpenSimplex
import numpy as np
from PIL import Image
import uuid
import math
import os
import datetime

class Map:

    def __init__(self, width, height, seed, overwright_val = {}, debug = False):

        self.width = width
        self.height = height
        self.seed = seed
        self.debug = debug

        self.val = {
            "bias" : 10,
            "octaves" : 11,
            "persistance" : 0.5,
            "lacunarity" : 2,
        }

        self.colors = [
            (0, 62, 178),
            (9, 82, 198),
            (20, 100, 210),
            (254, 224, 179),
            (9, 120, 93),
            (10, 107, 72),
            (11, 94, 51),
            (140, 142, 123),
            (160, 162, 143),
            (255, 255, 255)
        ]


        for i in list(overwright_val.keys()):
            if i in list(self.val.keys()):
                self.val[i] = overwright_val[i]
        
        self.heightMap = np.empty((self.height, self.width), dtype=np.short)
        self.renderMap = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def populateMap(self):
        #__--Definition of locals--__
        scale = max(self.width, self.height) / 4
        noise = OpenSimplex(seed=self.seed)

        if self.debug:
            print("Map Generation Debug Info:")
            print("Size:", self.width, "x", self.height)
            print("  Seed:", self.seed)
            starttime = datetime.datetime.now()
            print("  Start Time:", starttime)
            print("---------------")

        #__--The loop finds the noise value for each pixel and applys a quadratic falloff to make a island--__
        
        for y in range(0, self.height):    #Loops through every pixel
            for x in range(0, self.width): #------------------------

                #Defines the loop variables
                amplitude = 1
                frequency = 1
                noiseHeight = 0

                for octave in range(0, self.val["octaves"]):  #Loops through the octaves of each pixel
                    value = noise.noise3(x / scale * frequency, y / scale * frequency, 0) #Finds the raw noise value for the pixel
                    noiseHeight += value * amplitude #Applies the noise value to a running total through the octaves

                    amplitude *= self.val["persistance"] #Adjusts the modifiers for the next loop
                    frequency *= self.val["lacunarity"]  #--------------------------------------

                self.heightMap[y][x] = (noiseHeight + 1) * 128 #Applies product of the loop to the final array
                
                x_falloff = -((x-(self.width/2))**2)/(4**((math.log(self.width)/math.log(2))-1)) + 1   #Uses a quadratic to find the falloff value for the x and y
                y_falloff = -((y-(self.height/2))**2)/(4**((math.log(self.height)/math.log(2))-1)) + 1 #----------------------------------------------------------

                self.heightMap[y][x] *= (x_falloff + y_falloff)/2 #Averages the falloff and applies to the final

                if self.heightMap[y][x] > 255: #Failsafe to ensure products remain within bounds
                    self.heightMap[y][x] = 255
                elif self.heightMap[y][x] < 0:
                    self.heightMap[y][x] = 0

        if self.debug:
            endtime = datetime.datetime.now()
            print("  End Time:", endtime)
            print("  Delta:", endtime - starttime)
            print("---------------")


    def getColor(self, heightVal):
        if heightVal < 0:
            heightVal = 0
        if heightVal > 255:
            heightVal = 255

        if heightVal <= 84:
            return self.colors[0]
        elif heightVal <= 98:
            return self.colors[1]
        elif heightVal <= 110:
            return self.colors[2]
        elif heightVal <= 115:
            return self.colors[3]
        elif heightVal <= 134:
            return self.colors[4]
        elif heightVal <= 164:
            return self.colors[5]
        elif heightVal <= 200:
            return self.colors[6]
        elif heightVal <= 224:
            return self.colors[7]
        elif heightVal <= 242:
            return self.colors[8]
        elif heightVal <= 255:
            return self.colors[9]
        return self.colors[0]

    def renderTo(self, path = ""):


        if self.debug:
            print("Map Rendering Debug Info:")
            starttime = datetime.datetime.now()
            print("  Start Time:", starttime)
            print("---------------")
        
        #__--Render--__
        for y in range(0, self.height): #Loops through every pixel applying color values
            for x in range(0, self.width):
                height = self.heightMap[y][x]
                colour = self.getColor(height)
                self.renderMap[y][x] = colour

        image = Image.fromarray(self.renderMap, 'RGB') #numPy array to image rendering
    
        #__--File saving--__
        current_dir = os.path.dirname(os.path.abspath(__file__)) #Finds current directory
        files = os.listdir(current_dir + "/" + path)             #and lists files in target directory

        lastfilename = "Map_-1.png"
        for file in files:       #Finds the last saved map file
            if file[0:4] == "Map_":
                lastfilename = file
        
        newindex = int(lastfilename.split('_')[1].split('.')[0]) + 1

        image.save(current_dir + "/" + path + "/Map_" + str(newindex) + ".png") #Saves the image to the target directory with incremented index

        if self.debug:
            endtime = datetime.datetime.now()
            print("  Map saved to:", current_dir + "/" + path + "/Map_" + str(newindex) + ".png")
            print("  End Time:", endtime)
            print("  Delta", endtime - starttime)
            print("---------------")

if __name__ == "__main__":
    map = Map(128, 128, uuid.uuid4().int & (1<<16)-1, debug = True)
    map.populateMap()
    map.renderTo("maps")