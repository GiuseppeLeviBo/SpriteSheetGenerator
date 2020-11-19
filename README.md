############ Original README ##############
##Source code for the sprite sheet generator explained in  as as
https://minzkraut.com/2016/11/23/making-a-simple-spritesheet-generator-in-python/

##Usage:    
- Copy all your single frames into "frames/"  
- Optionally change `max_frames_row` on line 3 (How many frames until a linebreak happens)  asas
- Run `python2.7 createSpriteSheet.py`   
- Enjoy the sprite sheet that appeared in the folder  
#######################################################################

The modified version of the script generates the JSON file in order to load the sprites PHASER3 load.atlas function.
Using the same script (original and modified) it would be possible to generate a spritechart for animation ordering the frames in alfabetical order
in the frames folder.

