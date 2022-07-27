from ast import literal_eval as make_tuple
from pathlib import Path
from PIL import Image
import random
import json


def color2tuple(bg_info):
    if bg_info == 'w':
        return (255, 255, 255, 0)

    return None

def get_background(template, template_info):
    # If we're going not going to paste over image, we make a b/w layer
    if template_info['background'] != 'o':
        return Image.new('RGB', template.size, color2tuple(template_info['background']))
    else:
        return template

def get_unique_sources(template_info, template_num):
    """
    Gets unique source images to be used in template
    (whilst making sure it's not a duplicated meme)"""
    all_source_imgs = list(Path('./Source Images').rglob('*'))

    while True:
        src_imgs = []

        for box in template_info['boxes']:
            # If image is repeated, the source image is the same
            if 'repeat_prev' not in box:
                rand_src_img = random.choice(all_source_imgs)

            src_imgs.append(rand_src_img)

        meme_filename = f'{template_num}-{"-".join([img.stem for img in src_imgs])}.png'
        meme_filepath = Path(f'./Memes/{meme_filename}')

        # If meme has already been made -> select new src images
        # Otherwise
        if not meme_filepath.is_file():
            return src_imgs, meme_filepath

def make_meme(bg, template, template_info, src_imgs):
    for i, box in enumerate(template_info['boxes']):
        src = Image.open(src_imgs[i])

        # Box (Blank Area)
        size_x, size_y = make_tuple(box['size'])

        # Resizes image AND keeps aspect ratio
        ## Shrink
        if src.size[0] > size_x or src.size[1] > size_y:
            src.thumbnail((size_x, size_y), Image.LANCZOS)
        ## Enlarge
        else:
            hpercent = size_y / src.size[1]  # Magic pt. 1
            wsize = int(src.size[0] * hpercent)  # Magic 2: The Awakening
            src = src.resize((wsize, size_y))  # Magic 3: Revenge of the Syntax

            if src.size[0] > size_x :
                wpercent = size_x / src.size[0]  # Magic IV: A New Bug
                hsize = int(src.size[1] * wpercent)  # Magic 5: Wrath of Fam
                src = src.resize((size_x, hsize))  # Magic 6: The Return of the Bug

        # Coordinates of top left corner (where image is pasted)
        top_left = make_tuple(box['left_corner'])
        # Remaining space inside box (used for centering)
        blank_x = size_x - src.size[0]
        blank_y = size_y - src.size[1]

        # Pastes centered Source Image in Box
        bg.paste(src, (int(top_left[0] + blank_x / 2), int(top_left[1] + blank_y / 2)))

    # Overlay meme over background layer
    if template_info['background'] != 'o':
        bg.paste(template, (0, 0), template)

    return bg

if __name__ == "__main__":
    with open('sizes.json') as sizes:
        jsonData = json.load(sizes)

    all_templates = list(Path('./Templates').rglob('*'))
    template_path = random.choice(all_templates)
    template_info = jsonData[template_path.stem]

    template = Image.open(template_path)
    bg = get_background(template, template_info)
    src_imgs, meme_filepath = get_unique_sources(template_info, template_path.stem)
    meme = make_meme(bg, template, template_info, src_imgs)
    meme.save(meme_filepath)
