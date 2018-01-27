# Meme-Bot
A reversed engineered version of ShitpostBot 5000 using Pillow (PIL-fork)

## Instructions: 
* To add a template:

    You must **manually** capture the box where each source image will be pasted, inside `sizes.json`

    Inside `sizes.json` the legend goes as follows:
    * `background` = Background of the space where the source image is pasted. There are 3 options:
        * `b` = black background
        * `w` = white background
        * `o` = Over. Source Image is pasted on top of the template, there's no background
    * `boxes` = Is a list of the dictionaries (box) that contains info for box.
        
        Each box contains 2 keys that have tuples as values:
        * `size` = Size of the box
        * `left_corner` = Coordinates for the top-left corner of the box 
        * **Note**: if you want to repeat the same Source Image used before, but at different coordinates and/or size, you need to add a new key called `repeat_prev` with `True` value. This is used in `Templates/5.png`
    
**Side-note**: If you prefer the previously used [`sizes.txt` format](https://i.imgur.com/rLlIyhR.png) instead of the current `sizes.json`, you can use the current release along with a [script](https://gist.github.com/diegotf30/54c51ebad12ad90db19c365df0972392) I made to convert `sizes.txt` to JSON format.

* Regarding Source Images:

    Although not necessary, I recommend you to number the source images to easily identify the source images used in a given meme, since its filename is made using the format: `Template-SrcImg1-SrcImg2-...-SrcImgN.png` 
    
* Dependencies

    For the script to work you must have `Pillow` (a friendly PIL fork). You can install it using `pip install Pillow` or with `easy_install Pillow`. For more information on its documentation/installation go [here](http://pillow.readthedocs.io/en/stable/installation.html).
    
And ta-da! You're ready to make some dank -but most importantly- ***randomly generated*** memes. Have fun!

## Author's note:

If you wish to integrate the bot with Twitter I recommend this [repository](https://github.com/joaquinlpereyra/twitterImgBot), although the non-repeating image validation doesn't work (16/09/2017). 

My own fully-automated version: [@OlaSoyUnBot_](https://twitter.com/OlaSoyUnBot_)
