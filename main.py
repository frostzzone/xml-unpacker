"""
Python script to extract images from XML/PNG pairs (I've used it for FNF)
Scans the "d" directory for any XML and PNG pairs, and if it finds them, creates a new folder in the "out" directory with the same name as the images
Note that it won't output images in the "d" directory if they have no corresponding XML file

Requires os, PIL, BeautifulSoup, lxml (html reader for BeautifulSoup) and re
"""
# Change this to the game's images folder (the one with the textures and XML files). 
d = r"./input"

# Change this to the folder you want the final, separated textures to be outputted.
out = r"./output"

import os
from PIL import Image
from bs4 import BeautifulSoup
import re
import lxml

print("parsing")
for path, currentDirectory, files in os.walk(d):
    for file in files:
        if file.endswith(".xml"):
            print(f"! found {file}")
            namewithoutfile = file.split(".")[0]
            try:
                os.mkdir(out + "/" + file.split(".")[0])
            except:
                print(f"Already done {file}, continuing")
                continue
            wholeimage = Image.open(os.path.join(path, file.replace(".xml", ".png")))
            with open(os.path.join(path, file)) as xmldata:
                soup = BeautifulSoup(xmldata.read(), "lxml")
            allsubtx = soup.find_all("subtexture")
            uniquex = []
            uniquey = []
            for subtx in allsubtx:
                name = re.sub(r'[^A-Za-z0-9 _%]+', '', subtx["name"])
                left = int(subtx["x"])
                top = int(subtx["y"])
                if left in uniquex and top in uniquey and uniquey[uniquex.index(left)] == top:
                    continue
                else:
                    uniquex.append(left)
                    uniquey.append(top)
                right = left + int(subtx["width"])
                bottom = top + int(subtx["height"])
                subimg = wholeimage.crop((left, top, right, bottom))
                try:
                    subimg.save(f"{out}/{namewithoutfile}/{name}.png")
                    print(f"> saved {name}.png")
                except Exception as e:
                    print(f"!> error saving {name}.png - {e}")
print("done")