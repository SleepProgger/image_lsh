# TODO: Add command line arguments

from urllib2 import urlopen
from image_lsh import down_scale_rgb, rgb_to_gray, load_rgb_image
from image_lsh import ahash, dhash_h, dhash_v
from image_lsh.dbg import image_md5hex
import json



_default_hash_size = {
    'scaled_hash': [[11,11]], 'scaled_gray_hash': [[11,11]],
    'ahash': [[11,11]], 'dhash_h': [[12,11]], 'dhash_v': [[11,12]]
}
class LSH_Testcase_v_0_1():
    _VERSION = "0.1" 
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
        self.tests = list()
    
    def create_LSH_testcase_element(self, url, name=None, hash_sizes=_default_hash_size):
        test_case = {'url': url}
        if name: test_case['name'] = name
        data = urlopen(url)
        img = load_rgb_image(data)
        test_case['image_size'] = (img.shape[1], img.shape[0])
        test_case['image_hash'] = image_md5hex(img)
        if 'scaled_hash' in hash_sizes:
            tmp = list()
            for width, height in hash_sizes['scaled_hash']:
                tmp.append((width, height, image_md5hex(down_scale_rgb(img, width, height))))  
            test_case['scaled_hash'] = tmp 
        if 'scaled_gray_hash' in hash_sizes:
            tmp = list()
            for width, height in hash_sizes['scaled_gray_hash']:
                tmp.append((width, height, image_md5hex(rgb_to_gray(down_scale_rgb(img, width, height)))))  
            test_case['scaled_gray_hash'] = tmp 
        if 'ahash' in hash_sizes:
            tmp = list()
            for width, height in hash_sizes['ahash']:
                tmp.append((width, height, ahash(img, width, height)))  
            test_case['ahash'] = tmp 
        if 'dhash_h' in hash_sizes:
            tmp = list()
            for width, height in hash_sizes['dhash_h']:
                tmp.append((width, height, dhash_h(img, width, height)))  
            test_case['dhash_h'] = tmp 
        if 'dhash_v' in hash_sizes:
            tmp = list()
            for width, height in hash_sizes['dhash_v']:
                tmp.append((width, height, dhash_v(img, width, height)))  
            test_case['dhash_v'] = tmp 
        self.tests.append(test_case)
    
    
    def _pack(self):
        ret = {'version': self._VERSION, 'name': self.name}
        if self.description: ret['description'] = self.description
        ret['tests'] = self.tests
        return ret
    def dump(self, *args, **kwargs):
        json.dump(self._pack(), *args, **kwargs)
    def dumps(self, *args, **kwargs):
        json.dumps(self._pack(), *args, **kwargs)
        
    
    
    
if __name__ == '__main__':
    images = (
              'http://i.imgur.com/LEOaSRo.jpg',
              'http://i.imgur.com/oUSDbwN.jpg',
              )
    
    testcase = LSH_Testcase_v_0_1("LSH test", "Some description")
    for url in images:
        testcase.create_LSH_testcase_element(url, "")
        
    with open('test_testcase.json', 'wb') as fp:
        testcase.dump(fp, indent=2, sort_keys=True)
    
    
    
    
    