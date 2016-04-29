from image_lsh.lsh import _ahash, _dhash_h, _dhash_v

from image_lsh.imaging import load_rgb_image, rgb_to_gray, down_scale_rgb


def ahash(img, width=8, height=8):
    img = down_scale_rgb(img, width, height)
    img = rgb_to_gray(img)
    return _ahash(img)

def dhash_h(img, width=9, height=8):
    img = down_scale_rgb(img, width, height)
    img = rgb_to_gray(img)
    return _dhash_h(img)

def dhash_v(img, width=8, height=9):
    img = down_scale_rgb(img, width, height)
    img = rgb_to_gray(img)
    return _dhash_v(img)
    
