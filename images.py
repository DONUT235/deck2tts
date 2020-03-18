from PIL import Image
import urllib.request

def open_image(filename):
    return Image.open(filename)

def combine(imageData, grid_size, img_size, out):
    #TODO use pillow to build card sheet
    cur_row = 0
    cur_col = 0
    width = grid_size[0]*img_size[0]
    height = grid_size[1]*img_size[1]
    result = Image.new('RGB', (width, height))
    for img in imageData:
        box = (img_size[0]*cur_col, img_size[1]*cur_row)
        result.paste(img, box=box)
        cur_col = (cur_col + 1) % grid_size[0]
        if cur_col == 0:
            cur_row = (cur_row + 1) % grid_size[1]

    if width > 4096:
        height = int(height*4096/width)
        width = 4096
        result = result.resize((width, height))
    result.save(out)
    return result
