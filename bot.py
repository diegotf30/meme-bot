from ast import literal_eval as make_tuple
from PIL import Image
import random
import json
import os


def getBackgroundColor() :
    if tempInfo['background'] == 'w' :
        return (255, 255, 255, 0)

def getBackground() :
    # If we're going not going to paste over image, we make a b/w layer
    if tempInfo['background'] != 'o' :
        return Image.new('RGB', template.size, getBackgroundColor())
    else :
        return template

def getUniqueSources() :
    """
    Gets all source images to be used in template
    (making sure it's not a duplicated meme)"""

    while True :
        source_imgs = []

        for box in tempInfo['boxes'] :
            # If image is repeated, the source image is the same
            if 'repeat_prev' not in box :
                # Random source image (e.g. '98.png')
                rand_source = random.choice(os.listdir(source_dir))

            source_imgs.append(rand_source.split('.')[0])

        # Name for the file
        filename = f'{temp_num}-{"-".join(source_imgs)}.png'

        # If meme hasn't been done before, we continue with meme-making process
        if not os.path.isfile(os.path.join(memes_dir, filename)) :
            break

    return source_imgs, filename


def make_meme() :
    n = 0
    for box in tempInfo['boxes'] :
        src = Image.open(os.path.join(source_dir, f'{source_imgs[n]}.png'))

        # Box (Blank Area)
        size_x, size_y = make_tuple(box['size'])

        # Resizes image AND keeps aspect ratio
        ## Shrink
        if src.size[0] > size_x or src.size[1] > size_y :
            src.thumbnail((size_x, size_y), Image.LANCZOS)
        ## Enlarge
        else :
            hpercent = size_y / src.size[1]  # Magic pt. 1
            wsize = int(src.size[0] * hpercent)  # Magic 2: The Awakening
            src = src.resize((wsize, size_y))  # Magic 3: Revenge of the Syntax

            if src.size[0] > size_x  :
                wpercent = size_x / src.size[0]  # Magic IV: A New Hope
                hsize = int(src.size[1] * wpercent)  # Magic 5: Wrath of Fam
                src = src.resize((size_x, hsize))  # Magic 6: The Return of the Bug

        # Coordinates of top left corner (where image is pasted)
        top_left = make_tuple(box['left_corner'])
        # Remaining space inside box (used for centering)
        blank_x = size_x - src.size[0]
        blank_y = size_y - src.size[1]

        # Pastes centered Source Image in Box
        bg.paste(src, (int(top_left[0] + blank_x / 2), int(top_left[1] + blank_y / 2)))
        # Goes to next source image (if there is a space for it)
        n += 1

    # Overlay meme over background layer
    if tempInfo['background'] != 'o' :
        bg.paste(template, (0, 0), template)

    return bg


if __name__ == "__main__" :
    home_dir = os.path.dirname(os.path.realpath(__file__))
    temp_dir = os.path.join(home_dir, 'Templates')
    source_dir = os.path.join(home_dir, 'Source Images')
    memes_dir = os.path.join(home_dir, 'Memes')
    jsonFile = os.path.join(home_dir, 'sizes.json')

    with open(jsonFile) as sizes:
        jsonData = json.load(sizes)

    rand_template = random.choice(os.listdir(temp_dir))
    template = Image.open(os.path.join(temp_dir, rand_template))
    # Get template number, eliminates file extension
    temp_num = rand_template.split('.')[0]
    # Contains background color and box sizes
    tempInfo = jsonData[temp_num]

    bg = getBackground()

    source_imgs, filename = getUniqueSources()

    meme = make_meme()

    # Saves meme
    meme.save(os.path.join(memes_dir, filename))
