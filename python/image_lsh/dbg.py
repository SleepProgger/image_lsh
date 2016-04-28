from PIL import Image
from itertools import imap, izip
from operator import ne

def show_img_OCV(img):
    import cv2
    # expects RGB
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def show_img_PIL(img):
    # expects RGB
    img = Image.fromarray(img)
    print "SHOW PIL image", img
    img.show()
    
# We just always use PILs show (default imageviewer AFAIK)
# as default
show_img = show_img_PIL


def image_md5hex(img):
    from hashlib import md5
    return md5(img.flatten()).hexdigest().upper()

def change_count(a, b):
    ret = abs(len(a.flatten())-len(b.flatten()))
    print "len a,b, all", len(a.flatten()), len(b.flatten()), ret
    return ret + sum(imap(ne, a.flatten(), b.flatten()))
    