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

#template
bot = Image.open(temp_dir + rand_temp)

#source image
top = Image.open(source_dir + rand_source) 

width, height = bot.size
size = (width, height)

#Puts Source image in template
meme = ImageOps.fit(top, size, Image.ANTIALIAS)
meme.paste(bot, (0,0), bot)
char_set = string.ascii_uppercase + string.digits
meme.save( memes_dir + ''.join(random.sample(char_set*6, 6)) + '.png')
meme.show()
