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
    # If we're going not going to paste over image, we make an image of just b or w
    if bg_info != 'o' :
        return Image.new('RGB', temp.size, getBackgroundColor(bg_info))
    else :
        return temp

def getUniqueSources(tempInfo, memes_dir) :
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
        filename = temp_num + '-' + '-'.join(source_imgs) + '.png'

        # If meme hasn't been done before, we continue with meme-making process
        if not os.path.isfile(os.path.join(memes_dir, filename)) :
            break

    return source_imgs, filename


def make_meme(background, template, tempInfo, source_imgs) :
    boxes = tempInfo['boxes']
    bg_color = tempInfo['background']
    n = 0
    while n < len(source_imgs) :
        # Box (Blank Area) Properties
        size = make_tuple(boxes[n]['size'])
        size_x = size[0]
        size_y = size[1]

        src = Image.open(os.path.join(source_dir, f'{source_imgs[n]}.png'))

        # Resizes image AND keeps aspect ratio
        ## Shrink
        if src.size[0] > size_x or src.size[1] > size_y :
            src.thumbnail((size_x, size_y), Image.LANCZOS)
        ## Enlarge
        else :
            hpercent = (size_y / float(src.size[1]))  # Magic pt. 1
            wsize = int((float(src.size[0]) * float(hpercent)))  # Magic 2: The Awakening
            src = src.resize((wsize, size_y))  # Magic 3: Revenge of the Syntax

            if src.size[0] > size_x  :
                wpercent = (size_x / float(src.size[0]))  # Magic IV: A New Hope
                hsize = int((float(src.size[1]) * float(wpercent)))  # Magic 5: Wrath of Fam
                src = src.resize((size_x, hsize))  # Magic 6: The Return of the Bug

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
        background.paste(src, (int(paste_x + black_x / 2), int(paste_y + black_y / 2)))
        # Goes to next source image (if there is a space for it)
        n += 1

    # Puts Template on top of background (when background color = b/w)
    if bg_color != 'o' :
        background.paste(template, (0, 0), template)

    return background


if __name__ == "__main__" :
    home_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = os.path.join(home_dir, 'Templates')
    source_dir = os.path.join(home_dir, 'Source Images')
    memes_dir = os.path.join(home_dir, 'Memes')
    jsonFile = os.path.join(home_dir, 'sizes.json')

    with open(jsonFile) as sizes:
        jsonData = json.load(sizes)

    secure_random = random.SystemRandom()

    # Random template
    rand_temp = secure_random.choice(os.listdir(temp_dir))
    # Get template number, eliminates file extension
    temp_num = rand_temp.split('.')[0]
    # Template Image
    temp = Image.open(os.path.join(temp_dir, rand_temp))
    # Contains background color and box sizes
    tempInfo = jsonData[temp_num]

    background = getBackground(temp, tempInfo)

    source_imgs, filename = getUniqueSources(tempInfo, memes_dir)

    meme = make_meme(background, temp, tempInfo, source_imgs)

    # Saves meme
    meme.save(os.path.join(memes_dir, filename))
