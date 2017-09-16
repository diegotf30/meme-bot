from PIL import Image, ImageOps
import os, random
import re
import linecache
import string

home_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = home_dir + '\\Templates\\'
source_dir = home_dir + '\\Source\\'
memes_dir = home_dir + '\\Memes\\'

#Random template & source image
rand_temp = random.choice(os.listdir(temp_dir))
rand_source = random.choice(os.listdir(source_dir))

#Get template number
size_lst = re.findall(r'\d+', rand_temp) #workaround
size_index = int(''.join(size_lst)) + 2
#Retrieve box size from file
size_s = linecache.getline('sizes.txt',size_index)
#Blank Area Properties
size_x = int(size_s.split()[1])
size_y = int(size_s.split()[2])

#template
bot = Image.open(temp_dir + rand_temp)

#source image
top = Image.open(source_dir + rand_source)

#Resizes image to keep aspect ratio
##Shrink
if top.size[0] > size_x & top.size[1] > size_y :
    top.thumbnail((size_x,size_y), Image.LANCZOS)
##Enlarge
else:
    hpercent = (size_y / float(top.size[1])) #Magia pt. 1
    wsize = int((float(top.size[0]) * float(hpercent))) #Magia 2: The Awakening
    top = top.resize((wsize, size_y)) #Magia 3: Revenge of the Syntax

#Source Image Width
width = top.size[0]
#Blank Area - Source Image Width
black_area = size_x - width 
#Coordinates where image is pasted
x = int(size_s.split()[3])
y = int(size_s.split()[4])

#Puts Source image in template
bot.paste(top, (int(x + black_area/2),y))
char_set = string.ascii_uppercase + string.digits
bot.save(memes_dir + ''.join(random.sample(char_set*6, 6)) + '.png')



