from PIL import Image # Depends on the Pillow lib
from opensimplex import OpenSimplex
import math
import uuid
import os

print("Initiated\nBegin World Generation...")
print("  ...Defining Constants...")

WIDTH = 256
HEIGHT = 256
FEATURE_SIZE = 50.0
SEED = uuid.uuid1().int >> 64
NOISE = OpenSimplex(SEED)

COLOR_DEEPWATER = (0, 62, 178)
COLOR_WATER = (9, 82, 198)
COLOR_SAND = (254, 224, 179)
COLOR_GRASS = (9, 120, 93)
COLOR_DARKGRASS = (10, 107, 72)
COLOR_DARKESTGRASS = (11, 94, 51)
COLOR_DARKROCKS = (140, 142, 123)
COLOR_ROCKS = (160, 162, 143)
COLOR_SNOW = (255, 255, 255)


#gradientvalue = 128 - (abs((x - WIDTH/2)/2) + abs(( y - HEIGHT/2)/2))
#value = gradientvalue + noisevalue + 64

def FindColor(value):
  if value <= 84:
        return COLOR_DEEPWATER
  elif value <= 102:
        return COLOR_WATER
  elif value <= 112:
        return COLOR_SAND
  elif value <= 134:
        return COLOR_GRASS
  elif value <= 164:
        return COLOR_DARKGRASS
  elif value <= 200:
        return COLOR_DARKESTGRASS
  elif value <= 224:
        return COLOR_DARKROCKS
  elif value <= 242:
        return COLOR_ROCKS
  elif value <= 255:
        return COLOR_SNOW
  return COLOR_DEEPWATER

  return value
  
def main():
      print("  ...Begin Main Process...")
      print("    ...creating canvases...")
      imnoise = Image.new('P', (WIDTH, HEIGHT))
      imgradient = Image.new('P', (WIDTH, HEIGHT))
      imblended = Image.new('P', (WIDTH, HEIGHT))
      print("    ...generating values...")

  
      for y in range(0, HEIGHT):
            for x in range(0, WIDTH):
                  noisevalue = (NOISE.noise2(x / FEATURE_SIZE, y / FEATURE_SIZE)+1)* 128
                  distX = WIDTH/2 - abs(WIDTH / 2 - x)
                  distY = HEIGHT/2 -abs(HEIGHT / 2 - y)
                  dist = min(distX, distY)
                  gradientvalue = dist / max(WIDTH/2, HEIGHT/2) * 255
                  imnoise.putpixel((x, y), FindColor(noisevalue))
                  imgradient.putpixel((x, y), FindColor(gradientvalue))
                  imblended.putpixel((x, y), FindColor(noisevalue/2 + gradientvalue/2))

      print("    ...saving outputs...")

    
      current_dir = os.path.dirname(os.path.abspath(__file__))

      try:
            lastfilename = os.listdir(current_dir + "/maps")[-1]
            newindex = int(lastfilename[3:-4]) + 1
      except:
            newindex = 0
    

      imnoise.save(current_dir + "/maps/noise" + str(newindex) + ".png")
      imgradient.save(current_dir + "/maps/gradient" + str(newindex) + ".png")
      imblended.save(current_dir + "/maps/blended" + str(newindex) + ".png")
      print("  ...Main Process Done!...")


if __name__ == '__main__':
    main()


print("...Done!")