from PIL import Image
import os
import random
import re
import linecache

home_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = home_dir + '\\Templates\\'
source_dir = home_dir + '\\Source\\'
memes_dir = home_dir + '\\Memes\\'

#Random template
rand_temp = random.choice(os.listdir(temp_dir))
#Get template number
size_lst = re.findall(r'\d+', rand_temp) #workaround
size_index = int(''.join(size_lst)) + 2
#Retrieve blank area from file
size_s = linecache.getline('sizes.txt',size_index)

#Template
temp = Image.open(temp_dir + rand_temp)

#Background colour
##b - black
##w - white
##o - no bg
bg_color = size_s.split()[1]

if bg_color == 'b' :
    colour = 0
elif bg_color == 'w' :
    colour = (255, 255, 255, 0)

#Background
if bg_color != 'o' :
    backg = Image.new('RGB', temp.size, colour)
else :
    backg = temp

#Name for the file, eliminates '.png' from rand_temp
meme_name = [rand_temp[:-4]]

#Source image counter
n = 2

while size_s.split()[n] != 'x' :
    #Determines if the template repeats an image
    if size_s.split()[n] != 's' :
        #Random source image (e.g. '98.png')
        rand_source = random.choice(os.listdir(source_dir))
        meme_name.append(rand_source[:-4])
    else :
        n += 1
        
    #Blank Area Properties
    size_x = int(size_s.split()[n])
    size_y = int(size_s.split()[n + 1])

    #source image
    src = Image.open(source_dir + rand_source)

    #Resizes image to keep aspect ratio
    ##Shrink
    if src.size[0] > size_x | src.size[1] > size_y :
        src.thumbnail((size_x,size_y), Image.LANCZOS)
    ##Enlarge
    else :
        hpercent = (size_y / float(src.size[1])) #Magia pt. 1
        wsize = int((float(src.size[0]) * float(hpercent))) #Magia 2: The Awakening
        src = src.resize((wsize, size_y)) #Magia 3: Revenge of the Syntax

        if src.size[0] > size_x  :
            wpercent = (size_x / float(src.size[0])) #Magia IV: A New Hope
            hsize = int((float(src.size[1]) * float(wpercent))) #Magia 5: Wrath of Fam 
            src = src.resize((size_x, hsize)) #Magia 6: The Return of the Bug
    #Coordinates where image is pasted
    paste_x = int(size_s.split()[n + 2])
    paste_y = int(size_s.split()[n + 3])

    #Source Image Width
    width = src.size[0]
    height = src.size[1]
    #Blank Area - Source Image Width
    black_x = size_x - width
    black_y = size_y - height
    
    #Centers Source image in template
    backg.paste(src, (int(paste_x + black_x/2),int(paste_y + black_y/2)))
    #Goes to next source image (if there is a space for it)
    n += 4

#Puts Template on top of background
backg.paste(temp, (0,0), temp)
#Random filename
#Saves meme
backg.save(memes_dir + '-'.join(meme_name) + '.png')
