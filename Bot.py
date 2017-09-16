from PIL import Image, ImageOps
import os, random
import re
import linecache
import string

home_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = home_dir + '\\Templates\\'
source_dir = home_dir + '\\Source Images\\'
memes_dir = home_dir + '\\Memes\\'


#Random template
rand_temp = random.choice(os.listdir(temp_dir))

#Get template number
size_lst = re.findall(r'\d+', rand_temp) #workaround
size_index = int(''.join(size_lst)) + 2
#Retrieve blank area from file
size_s = linecache.getline('sizes.txt',size_index)

#template
temp = Image.open(temp_dir + rand_temp)
#black background
backg = Image.new('RGB', temp.size)

#Source image counter
n = 1

while size_s.split()[n] != 'x' :
    #Random source image
    rand_source = random.choice(os.listdir(source_dir))

    #Blank Area Properties
    size_x = int(size_s.split()[n])
    size_y = int(size_s.split()[n + 1])

    #source image
    src = Image.open(source_dir + rand_source)

    #Resizes image to keep aspect ratio
    ##Shrink
    if src.size[0] > size_x & src.size[1] > size_y :
        src.thumbnail((size_x,size_y), Image.LANCZOS)
    ##Enlarge
    else:
        hpercent = (size_y / float(src.size[1])) #Magia pt. 1
        wsize = int((float(src.size[0]) * float(hpercent))) #Magia 2: The Awakening
        src = src.resize((wsize, size_y)) #Magia 3: Revenge of the Syntax

    #Source Image Width
    width = src.size[0]
    #Blank Area - Source Image Width
    black_area = size_x - width 
    #Coordinates where image is pasted
    paste_x = int(size_s.split()[n + 2])
    paste_y = int(size_s.split()[n + 3])
    #Puts Source image in backgroud
    backg.paste(src, (int(paste_x + black_area/2),paste_y))
    #Goes to next source image (if there is a space for it)
    n = n + 4

#Puts Template on top of background
backg.paste(temp, (0,0), temp)

#Random filename
char_set = string.ascii_uppercase + string.digits
backg.save(memes_dir + ''.join(random.sample(char_set*6, 6)) + '.png')
    
