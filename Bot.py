from os.path import join, isfile, dirname, realpath
from ast import literal_eval as make_tuple
from os import listdir
from PIL import Image
import random
import json


def getFilename(file):
    return file.split('.')[0]

def getBackground(template, background_type) :
    'Returns PIL Image object to be used as background'
    # Pasting over image, no need for background layer
    if background_type == 'o' :
        return template

    bg_color = (255, 255, 255, 0) if background_type == 'w' else 0
    return Image.new('RGB', template.size, bg_color)

def getUniqueSources() :
    """
    Gets all source images to be used in template
    (making sure it's not a duplicated meme)
    """

    i, max_tries = (0, 100)
    while i < max_tries :
        source_imgs = []

        for box in tempInfo['boxes'] :
            # If image is repeated, the source image is the same
            if 'repeat_prev' not in box :
                rand_source = random.choice(listdir(source_dir))

            source_imgs.append(getFilename(rand_source))

        filename = f'{temp_num}-{"-".join(source_imgs)}.png'

        # If meme hasn't been done before, we continue with meme-making process
        if not isfile(join(memes_dir, filename)) :
            break

        i += 1

    return source_imgs, filename


def generateMeme() :
    for i, box in enumerate(tempInfo['boxes']) :
        src = Image.open(join(source_dir, f'{source_imgs[i]}.png'))

        # Box (Blank Area)
        size_x, size_y = make_tuple(box['size'])

        # Resizes image AND keeps aspect ratio
        ## Shrink
        if src.size[0] > size_x or src.size[1] > size_y :
            src.thumbnail((size_x, size_y), Image.LANCZOS)
        ## Enlarge
        else :
            hpercent = size_y / src.size[1]  # Magic pt. 1
            wsize = int(src.size[0] * hpercent)  # Magic 2: The (git) Clone Wars
            src = src.resize((wsize, size_y))  # Magic 3: Revenge of the Syntax

            if src.size[0] > size_x  :
                wpercent = size_x / src.size[0]  # Magic IV: A New Bug
                hsize = int(src.size[1] * wpercent)  # Magic 5: 
                src = src.resize((size_x, hsize))  # Magic 6: The Return of the Bug

        # Coordinates where image is going to be pasted
        top_left = make_tuple(box['left_corner'])

        # Center image inside box
        centered_x = top_left[0] + (size_x - src.size[0]) // 2
        centered_y = top_left[1] + (size_y - src.size[1]) // 2

        # Pastes centered Source Image in Box
        bg.paste(src, (centered_x, centered_y))

    # Overlay meme over background layer
    if tempInfo['background'] != 'o' :
        bg.paste(template, (0, 0), template)

    return bg


if __name__ == "__main__" :
    home_dir = dirname(realpath(__file__))
    temp_dir = join(home_dir, 'Templates')
    source_dir = join(home_dir, 'Source Images')
    memes_dir = join(home_dir, 'Memes')
    jsonFile = join(home_dir, 'sizes.json')

    with open(jsonFile) as sizes:
        jsonData = json.load(sizes)

    rand_template = random.choice(listdir(temp_dir))
    template = Image.open(join(temp_dir, rand_template))
    # Get template number, eliminates file extension
    temp_num = getFilename(rand_template)
    # Contains background color and box sizes
    tempInfo = jsonData[temp_num]

    bg = getBackground(template, tempInfo['background'])

    source_imgs, filename = getUniqueSources()

    meme = generateMeme()

    # Saves meme
    meme.save(join(memes_dir, filename))
