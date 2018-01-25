from ast import literal_eval as make_tuple
from PIL import Image
import random
import json
import os


def getBackgroundColor(bg_info) :
    # Black
    if bg_info is 'b' :
        return 0
    # White
    elif bg_info is 'w' :
        return (255, 255, 255, 0)

def getBackground(temp, tempInfo) :
    # Background color
    bg_info = tempInfo['background']
    #If we're going not going to paste over image, we make an image of just b or w
    if bg_info != 'o' :
        return Image.new('RGB', temp.size, getBackgroundColor(bg_info))
    else :
        return temp

def getUniqueSources(tempInfo) :
    """
    Gets all source images to be used in template
    (makes sure it's not a duplicated meme)"""

    # Counter for boxes
    n = 0

    while True :
        source_imgs = []

        for box in tempInfo['boxes'] :
            # If image is repeated, the source image is the same
            if 'repeat_prev' not in box :
                # Random source image (e.g. '98.png')
                rand_source = secure_random.choice(os.listdir(source_dir))
                source_index = rand_source.split('.')[0]
            # Random source index (e.g. '98')
            source_imgs.append(source_index)

            n += 1

        # Name for the file
        meme_name = temp_num + '-' + '-'.join(source_imgs) + '.png'

        # If meme duplicated, runs loop again (gets different src images)
        with open(meme_log) as log :
            for line in log :
                if meme_name in line :
                    break
            else :
                break

    return source_imgs, meme_name


def make_meme(background, source_imgs, boxes, twitter_pic = None) :
    n = 0
    while n < len(source_imgs) :
        # Box (Blank Area) Properties
        size = make_tuple(boxes[n]['size'])
        size_x = size[0]
        size_y = size[1]

        # Source image
        if twitter_pic is None :
            src = Image.open(source_dir + source_imgs[n] + '.png')
        else :
            src = twitter_pic

        # Resizes image AND keeps aspect ratio
        ## Shrink
        if src.size[0] > size_x or src.size[1] > size_y :
            src.thumbnail((size_x,size_y), Image.LANCZOS)
        ## Enlarge
        else :
            hpercent = (size_y / float(src.size[1])) #Magic pt. 1
            wsize = int((float(src.size[0]) * float(hpercent))) #Magic 2: The Awakening
            src = src.resize((wsize, size_y)) #Magic 3: Revenge of the Syntax

            if src.size[0] > size_x  :
                wpercent = (size_x / float(src.size[0])) #Magic IV: A New Hope
                hsize = int((float(src.size[1]) * float(wpercent))) #Magic 5: Wrath of Fam
                src = src.resize((size_x, hsize)) #Magic 6: The Return of the Bug

        # Coordinates of top left corner (where image is pasted)
        top_left = make_tuple(boxes[n]['left_corner'])
        paste_x = top_left[0]
        paste_y = top_left[1]

        # Source Image Width
        width = src.size[0]
        height = src.size[1]
        # Blank Area - Source Image Width
        black_x = size_x - width
        black_y = size_y - height
        # Pastes centered Source Image in Template
        background.paste(src, (int(paste_x + black_x/2), int(paste_y + black_y/2)))
        # Goes to next source image (if there is a space for it)
        n += 1
    return background

if __name__ == "__main__" :
    home_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = home_dir + '\\Templates\\'
    source_dir = home_dir + '\\Source\\'
    memes_dir = home_dir + '\\Memes\\'
    meme_log = home_dir + '\\Twitter\\log'

    with open(home_dir + '\\sizes.json') as sizes:
        jsonData = json.load(sizes)

    secure_random = random.SystemRandom()

    # Random template
    # rand_temp = secure_random.choice(os.listdir(temp_dir))
    rand_temp = '213.png'
    # Get template number, eliminates file extension
    temp_num = rand_temp.split('.')[0]
    # Template Image
    temp = Image.open(temp_dir + rand_temp)
    # Contains background color and box sizes
    tempInfo = jsonData[temp_num]

    background = getBackground(temp, tempInfo)

    source_imgs, meme_name = getUniqueSources(tempInfo)

    meme = make_meme(background, source_imgs, tempInfo['boxes'])

    # Puts Template on top of background (when background color = b/w)
    if tempInfo['background'] != 'o' :
        meme.paste(temp, (0,0), temp)

    # Saves meme
    meme.save(memes_dir + meme_name)
