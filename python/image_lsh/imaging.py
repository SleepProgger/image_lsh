import numpy as np

# TODO: PY3
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
    
import logging
log = logging.getLogger("image_lsh")

# TODO: fix python/numpy downscale version and make opencv optional    
__has_ocv = False
try:
    import cv2
    __has_ocv = True
except ImportError:
    raise
    
from PIL import Image


# We are using PIL here because opencv doesn't support GIFs FE.
def load_rgb_image(data):
    """ Loads an image from the given data and convert it to RGB """
    if not hasattr(data, 'read'):
        data = StringIO(data)
    data = np.array(Image.open(data).convert('RGB'))
    return data


def down_scale_rgb_ocv(img, width, height):
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
def down_scale_rgb_np(img, width, height):
    raise NotImplementedError()
    # This kind of works, but completely ignores the cases
    # where on source pixel maps to 2 destination pixel
    # Also it looks like there is an off by one error somewhere in there
    dw, dh = int(width), int(height)
    tmp_dest = np.zeros((dh, dw, img.shape[2]), np.float32)
    sh, sw, _ = img.shape
    scaleX = np.float32(float(sw) / float(dw))
    scaleY = np.float32(float(sh) / dh)
    scaleXY = np.float32(scaleX * scaleY)
    block_y = int(scaleY)
    block_x = int(scaleX)
    print "Scaling (%i,%i) => (%i,%i)" % (sh, sw, dh, dw)
    print "Source pixel per destination pixel:", scaleXY
    scaleX_s = np.float32(dw / float(sw))
    scaleY_s = np.float32(dh / float(sh))
    scaleXY_s = np.float32(scaleX_s * scaleY_s)
    scale_vec = np.array([scaleXY_s]*img.shape[2], np.float32)
    dy = 0
    while dy < dh:
        sy = dy * scaleY
        isy = int(sy)
        dx = 0
        sx = np.float32(0)
        while dx < dw:
            isx = int(sx)        
            tmp_dest[dy, dx] = np.einsum('k,ijk -> k', scale_vec, img[isy : isy + block_y, isx :  isx + block_x])
            sx += scaleX    
            dx += 1
        dy += 1
    ret = np.ndarray((height, width, img.shape[2]), np.ubyte)
    np.around(tmp_dest, out=ret, decimals=0)
    return ret

down_scale_rgb = down_scale_rgb_ocv if __has_ocv else down_scale_rgb_np


def rgb_to_gray(img):
    weights = np.array((0.299, 0.587, 0.114), np.float32)
    ret = np.ndarray((img.shape[:2]), np.ubyte)
    np.around(np.einsum('k,ijk->ij', weights, img), out=ret, decimals=0)
    return ret
      
    