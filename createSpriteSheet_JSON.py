#Original code by Jan Gross with added JSON file generation for PHASER3 https://phaser.io/ game framework
# Added also a very basic support to multiple sized sprites.
#preload: function () // PHASER3 function to load Graphics
#    {                              
#    //                              The Sprite Sheet            The JSON FILE
#        this.load.atlas('assets', './breakout/breakout.png', './breakout/breakout.json');
#    }
#
from PIL import Image
import os, math, time,json
from json import JSONEncoder
#Classes for JSON file generation
class frame():
   def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
class spriteSourceSize():
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
class sourceSize():
    def __init__(self,w,h):
        self.w = w
        self.h = h
class pivot():
    def __init__(self,x,y):
        self.x = x
        self.y = y
class sprite():
    def __init__(self,frame,spriteSourceSize,sourceSize,pivot):
        self.frame=frame
        self.spriteSourceSize=spriteSourceSize
        self.sourceSize=sourceSize
        self.rotated = False
        self.trimmed = False
        self.pivot = pivot
# Costum JSON encoder
class SpriteEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
	
max_frames_row = 10.0
frames = []
#names of files are used to identify sprites in JSON file
names =[]
tile_width = 0
tile_height = 0

spritesheet_width = 0
spritesheet_height = 0

files = os.listdir("frames/")
files.sort()
for current_file in files :
    try:
        with Image.open("frames/" + current_file) as im :
            frames.append(im.getdata())
# Just the name is saved not the extension
            names.append(os.path.splitext(current_file)[0])
    except:
        print(current_file + " is not a valid image")
# The maximum dimension of the sprite is taken as  'tile' dimension
# This will create a sheet with some white spaces. But Optimization is not the goal of the simple script
tile_width = max(fr.size[0] for fr in frames)
tile_height = max(fr.size[1] for fr in frames)
print(tile_height)
print(tile_width)
print(names)

if len(frames) > max_frames_row :
    spritesheet_width = tile_width * max_frames_row
    required_rows = math.ceil(len(frames)/max_frames_row)
    spritesheet_height = tile_height * required_rows
else:
    spritesheet_width = tile_width*len(frames)
    spritesheet_height = tile_height
    

spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))

#for current_frame in frames :
TheDict = {}
for j in range(len(frames)):
    current_frame = frames[j]
    current_name =names[j]
    current_tile_width = current_frame.size[0]
    current_tile_height = current_frame.size[1]
    top = tile_height * math.floor((frames.index(current_frame))/max_frames_row)
    left = tile_width * (frames.index(current_frame) % max_frames_row)
    bottom = top + tile_height
    right = left + tile_width
# Generates the class instancences
    FR  = frame(left,top,current_tile_width,current_tile_height)
    SpSsiz = spriteSourceSize(0,0,current_tile_width,current_tile_height)
    Ssiz=sourceSize(current_tile_width,current_tile_height)
    Pv=pivot(0.5,0.5)
    Sp=sprite(FR,SpSsiz,Ssiz,Pv)
# put each intance in a dictionary
    TheDict[current_name]=Sp
    box = (left,top,right,bottom)
    box = [int(i) for i in box]
    cut_frame = current_frame.crop((0,0,tile_width,tile_height))
    
    spritesheet.paste(cut_frame, box)
#compute the time string so that is equal for both files
timestr=time.strftime("%Y-%m-%dT%H-%M-%S")
#write the png
spritesheet.save("spritesheet" + timestr + ".png", "PNG")
#encode each class instance as JSON and convert the dictiory to a string
d2 = str({k: SpriteEncoder().encode(v) for k, v in TheDict.items()}) 
#Do some "by hand" string replace to obtain a final valid JSON and put some end of line to make it readable
d2= d2.replace("}'","}")
d2= d2.replace("'{","{\n")
d2= d2.replace("'","\"")
d2= d2.replace(",",",\n")
d2= "{\"frames\":"+d2+"}"
f = open("jsonfile"+timestr +".json", "w")
f.write(d2)
f.close()
