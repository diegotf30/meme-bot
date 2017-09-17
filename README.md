# Meme-Bot
A reversed engineered version of ShitpostBot 5000 using Pillow (PIL-fork)

## Instructions: 
* To add a template:

    You must **manually** capture the box where each source image will be pasted, inside `sizes.txt`

    Inside `sizes.txt` the legend goes as follows:
    * `bg_col` = Background of the space where the source image is pasted. There are 3 options:
        * `b` = black background
        * `w` = white background
        * `o` = Over. Source Image is pasted on top of the template, there's no background
    * `size_x` = Size of the box's x-axis (where the Source Image will be pasted)
        * Note: if you want to repeat the same Source Image used before, but at different coordinates, just put 's' in this column, and then input the box properties in the next 4 spaces. This is used in `Templates/5.png`
    * `size_y` = Size of the box's y-axis
    * `init_x` = x-coordinate of the box's top left corner
    * `init_y` = y-coordinate of the box's top left corner
    
    **Note:** `bg_col` only needs to be inputted once per template (as shown in the `sizes.txt` file example), while the rest of the values are inputted once per box, i.e. in `Templates/1.png` you would input 6 different `size_x`, `size_y`, `init_x` and `init_y` 
    
* Regarding Source Images:

    Although not necessary, I recommend you to number the source images to easily identify the source images used in a given meme, since its filename is made using the format: `Template-SrcImg1-SrcImg2-...-SrcImgN.png` 
    
* Dependencies

    For the script to work you must have `Pillow` (a friendly PIL fork). You can install it using `pip install Pillow` or with `easy_install Pillow`. For more information on its documentation/installation go [here](http://pillow.readthedocs.io/en/stable/installation.html).
    
And ta-da! You're ready to make some dank -but most importantly- ***randomly generated*** memes. Have fun!
    
## To-do:
* Make the script modular

## Author's note:

If you wish to integrate the bot with Twitter I recommend this [repository](https://github.com/joaquinlpereyra/twitterImgBot), although the non-repeating image validation doesn't work (16/09/2017). 

My own fully-automated version: [@SnuppoBotto](https://twitter.com/SnuppoBotto)
