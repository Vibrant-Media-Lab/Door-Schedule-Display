import requests
from io import BytesIO
from PIL import Image

def repalette(input_img):
    input_palette = input_img.getpalette()
    # extract color data (assuming grayscale colors, so R = G = B)
    grayscale_colors = [input_palette[i] for i in [0, 3, 6]]
    
    # Sort by darkest -> lightest
    sorted_indices = sorted(range(len(grayscale_colors)), key=lambda idx: grayscale_colors[idx])
    # new colors are black, red, white
    brw_values = [(0, 0, 0), (255, 0, 0), (255, 255, 255)]

    # Create a new palette with the new colors mapped to sorted indices
    brw_palette = [0] * len(input_palette)
    for new_idx, old_idx in enumerate(sorted_indices):
        brw_palette[old_idx * 3: old_idx * 3 + 3] = brw_values[new_idx]

    # need to save as black-only and red-only images for the waveshare display
    # black is black, white, and white instead of BRW
    bww_values = [(0, 0, 0), (255, 255, 255), (255, 255, 255)]
    bww_palette = [0] * len(input_palette)
    for new_idx, old_idx in enumerate(sorted_indices):
        bww_palette[old_idx * 3: old_idx * 3 + 3] = bww_values[new_idx]
    input_img.putpalette(bww_palette)
    input_img.save(output_image_dir+"image_black.bmp")
    
    # Now, black and white are saved as white and the red is saved as black
    wrw_values = [(255, 255, 255), (0, 0, 0), (255, 255, 255)]
    wrw_palette = [0] * len(input_palette)
    for new_idx, old_idx in enumerate(sorted_indices):
        wrw_palette[old_idx * 3: old_idx * 3 + 3] = wrw_values[new_idx]
    input_img.putpalette(wrw_palette)
    input_img.save(output_image_dir+"image_red.bmp")
    

    # Apply the new palette
    input_img.putpalette(brw_palette)
    # input_img.show()
    return input_img
    
def binary_repalette(input_img):
    input_palette = input_img.getpalette()
    # extract color data (assuming grayscale colors, so R = G = B)
    grayscale_colors = [input_palette[i] for i in [0, 3]]
    
    # Sort by darkest -> lightest
    sorted_indices = sorted(range(len(grayscale_colors)), key=lambda idx: grayscale_colors[idx])
    # new colors are black, and white only
    new_colors = [(0, 0, 0), (255, 255, 255)]

    # Create a new palette with the new colors mapped to proper indices
    new_palette = [0] * len(input_palette)
    for new_idx, old_idx in enumerate(sorted_indices):
        new_palette[old_idx * 3: old_idx * 3 + 3] = new_colors[new_idx]

    # Apply the new palette
    input_img.putpalette(new_palette)
    input_img.save(output_image_dir+"image_black.bmp")
    # input_img.show()
    return input_img

def image_to_rbw(input_image, num_colors):
    """
    Convert an image to only use red, white, and black colors.

    Args:
        input_image: a PIL image object, in RGB mode.
    """

    # testing whether it looks better to downsize to the proper dimension and THEN convert to grayscale,
    # or to convert to grayscale then downsize. Regardless, applying a 3-color palette after 
    # grayscaling seems to work better
    # downsize_gray = input_image.resize((IMAGE_DIMENSION,IMAGE_DIMENSION)).convert("L").convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    gray_downsize = input_image.convert("L").resize((IMAGE_DIMENSION,IMAGE_DIMENSION)).convert('P', palette=Image.ADAPTIVE, colors=num_colors)
    
    # if the colors are similar shades, use only bw instead. This is because they are likely the same color and 
    # the algorithm is only picking up a little bit of noise
    close_colors = False
    if num_colors == 3:
        close_threshold = 20
        gray_palette = [gray_downsize.getpalette()[i] for i in [0, 3, 6]]
        print(gray_palette)
        if abs(gray_palette[0]-gray_palette[1]) < close_threshold: close_colors = True
        if abs(gray_palette[0]-gray_palette[2]) < close_threshold: close_colors = True
        if abs(gray_palette[1]-gray_palette[2]) < close_threshold: close_colors = True

    if close_colors:
        image_to_rbw(gray_downsize, num_colors=2)
    if num_colors == 2:
        return binary_repalette(gray_downsize)
    else:
        return repalette(gray_downsize)

def is_grayscale_image(input_image):
    contains_non_grayscale = False
    for x in range(input_image.width):
        for y in range(input_image.height):
            r, g, b = input_image.getpixel((x, y))  # Get RGB values
            if r != g or g != b:  # Check if R, G, and B are not the same
                contains_non_grayscale = True
                break
        if contains_non_grayscale:
            break

    # Print the result
    if contains_non_grayscale:
        print("The image contains non-grayscale colors.")
        return False
    else:
        print("The image contains only grayscale colors.")
        return True

def image_to_bw(input_image, threshold=130):
    # Adjust this value to control the threshold for black/white conversion
    grayscale_image = input_image.convert("L")
    bw_image = grayscale_image.point(lambda p: 255 if p > threshold else 0)
    # bw_image.show()
    bw_image.save(output_image_dir+"image_black.bmp")
    return bw_image.resize((IMAGE_DIMENSION, IMAGE_DIMENSION))

def get_image_from_site(url):
    response = requests.get(url)
    if response.status_code == 200:
        site_image = Image.open(BytesIO(response.content))
        # Converting to RGB first to deal with potentially transparent areas
        if(site_image.mode=="RGBA"):
            print("converting RGBA to RGB")
            white_background = Image.new("RGB", site_image.size, (255, 255, 255))
            site_image = Image.alpha_composite(white_background.convert("RGBA"), site_image).convert("RGB")
        if(site_image.mode != "RGB"):
            site_image = site_image.convert("RGB")
        return site_image
    else:
        print(f"Failed to retrieve image. Status code: {response.status_code}")
        return None
    
def get_image_local(file_path):
    local_image = Image.open(file_path)
    
    # Converting to RGB first to deal with potentially transparent areas
    if(local_image.mode=="RGBA"):
            print("converting RGBA to RGB")
            white_background = Image.new("RGB", local_image.size, (255, 255, 255))
            local_image = Image.alpha_composite(white_background.convert("RGBA"), local_image).convert("RGB")
    if(local_image.mode != "RGB"):
        local_image = local_image.convert("RGB")

    return local_image

def open_image(path, how):
    """
    Open an image file locally or from the internet (.jpg and .png tested)

    Args:
        path (str): Path to the input image file or URL
        how (str): specify "local" to search path as local directory, "web" to fetch from online
    """
    if how == "web":
        return get_image_from_site(path)
    if how == "local":
        return get_image_local(path)

IMAGE_URL = "https://www.vml.pitt.edu/images/sign.png"
IMAGE_DIMENSION = 250 # assuming input to e-ink displaay will be a square of side length 250px
input_image_path = ""  # Replace with the path to your input JPEG image
output_image_dir = "/home/vml/display_imgs/"  # Replace with the desired output path

my_image = open_image(IMAGE_URL, "web")
if is_grayscale_image(my_image):
    image_to_bw(my_image)
else:
    image_to_rbw(my_image, 3)

# downloaded_image = open_image(IMAGE_URL, "web")
# downloaded_image.show()
# if is_grayscale_image(downloaded_image):
#     image_to_bw(downloaded_image, threshold=130).save()