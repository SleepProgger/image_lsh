from itertools import imap
from sys import version_info
if version_info > (3,0): # thats correct isn't it ?
    long = int 

######################
# For now all LSHs return "binary strings"
# because i am not sure about the endianess.
# In the long run they should just return python 
# integers/longs.
# So far if needed: 
######################
_bin_str_to_long = lambda x: long(x, base=2)


def _ahash(img):
    pix = img.flatten()
    avg_ = int( (pix.sum() / float(img.shape[0]*img.shape[1])) + 0.5)
    bits = str("".join(imap(lambda x: '1' if x < avg_ else '0', pix)))
    return bits

def _dhash_h(img):
    ret = ""
    _range = range(1, img.shape[1])
    for row in img:
        for x in _range:
            ret += "1" if row[x-1] < row[x] else "0"
    return ret

def _dhash_v(img):
    ret = ""
    _range_x = range(0, img.shape[1])
    for y in xrange(1, img.shape[0]):
        for x in _range_x:
            ret += "1" if img[y-1][x] < img[y][x] else "0"
    return ret