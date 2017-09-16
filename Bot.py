from PIL import Image
import os, random
import linecache

home_dir = os.path.dirname(os.path.realpath(__file__))
temp_dir = home_dir + '\\Templates\\'
source_dir = home_dir + '\\Source Images\\'
memes_dir = home_dir + '\\Memes\\'

secure_random = random.SystemRandom()

#Random template
rand_temp = secure_random.choice(os.listdir(temp_dir))
#Get template number, eliminates file extension
temp_num = rand_temp.split('.')[0]
sizes_index = int(''.join(temp_num)) + 2
#Retrieve template properties from 'sizes.txt'
sizes_str = linecache.getline('sizes.txt',sizes_index).split()

#Template
temp = Image.open(temp_dir + rand_temp)

#Background colour
##b - black
##w - white
##o - no bg
bg_color = sizes_str[1]

if bg_color == 'b' :
    colour = 0
elif bg_color == 'w' :
    colour = (255, 255, 255, 0)

#Background
if bg_color != 'o' :
    backg = Image.new('RGB', temp.size, colour)
else :
    backg = temp

#Name for the file
meme_name = temp_num.split(' ')

#Puts Counter in first box
n = 2

while n < len(sizes_str) :
    #Determines if the template repeats an image
    if sizes_str[n] != 's' :
        #Random source image (e.g. '98.png')
        rand_source = secure_random.choice(os.listdir(source_dir))
        #Random source index (e.g. '98')
        meme_name.append(rand_source.split('.')[0])
    else :
        n += 1
    
    #Blank Area Properties
    size_x = int(sizes_str[n])
    size_y = int(sizes_str[n + 1])

    #source image
    src = Image.open(source_dir + rand_source)

    #Resizes image AND keeps aspect ratio
    ##Shrink
    if src.size[0] > size_x or src.size[1] > size_y :
        src.thumbnail((size_x,size_y), Image.LANCZOS)
    ##Enlarge
    else :
        hpercent = (size_y / float(src.size[1])) #Magic pt. 1
        wsize = int((float(src.size[0]) * float(hpercent))) #Magic 2: The Awakening
        src = src.resize((wsize, size_y)) #Magic 3: Revenge of the Syntax

        if src.size[0] > size_x  :
            wpercent = (size_x / float(src.size[0])) #Magic IV: A New Hope
            hsize = int((float(src.size[1]) * float(wpercent))) #Magic 5: Wrath of Fam 
            src = src.resize((size_x, hsize)) #Magic 6: The Return of the Bug
            
    #Coordinates where image is pasted
    paste_x = int(sizes_str[n + 2])
    paste_y = int(sizes_str[n + 3])

    #Source Image Width
    width = src.size[0]
    height = src.size[1]
    #Blank Area - Source Image Width
    black_x = size_x - width
    black_y = size_y - height
    #Pastes centered Source Image in Template
    backg.paste(src, (int(paste_x + black_x/2),int(paste_y + black_y/2)))
    #Goes to next source image (if there is a space for it)
    n += 4

#Puts Template on top of background (when bg_col = b/w)
backg.paste(temp, (0,0), temp)
#Saves meme
backg.save(memes_dir + '-'.join(meme_name) + '.png')
