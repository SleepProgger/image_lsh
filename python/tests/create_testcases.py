# TODO: Fix the help text and think about the params.
# TODO: Make version aware when required
# TODO: Make scaling algo selectable (.. implement openCV replacement). 

from urllib2 import urlopen
from image_lsh import down_scale_rgb, rgb_to_gray, load_rgb_image
from image_lsh import ahash, dhash_h, dhash_v
from image_lsh.dbg import image_md5hex
import json
import sys



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
        if 'scaled_hash' in hash_sizes and len(hash_sizes['scaled_hash']) > 0:
            tmp = list()
            for width, height in hash_sizes['scaled_hash']:
                tmp.append((width, height, image_md5hex(down_scale_rgb(img, width, height))))  
            test_case['scaled_hash'] = tmp 
        if 'scaled_gray_hash' in hash_sizes and len(hash_sizes['scaled_gray_hash']) > 0:
            tmp = list()
            for width, height in hash_sizes['scaled_gray_hash']:
                tmp.append((width, height, image_md5hex(rgb_to_gray(down_scale_rgb(img, width, height)))))  
            test_case['scaled_gray_hash'] = tmp 
        if 'ahash' in hash_sizes and len(hash_sizes['ahash']) > 0:
            tmp = list()
            for width, height in hash_sizes['ahash']:
                tmp.append((width, height, ahash(img, width, height)))  
            test_case['ahash'] = tmp 
        if 'dhash_h' in hash_sizes and len(hash_sizes['dhash_h']) > 0:
            tmp = list()
            for width, height in hash_sizes['dhash_h']:
                tmp.append((width, height, dhash_h(img, width, height)))  
            test_case['dhash_h'] = tmp 
        if 'dhash_v' in hash_sizes and len(hash_sizes['dhash_v']) > 0:
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
        
    
import re
def SizeType(v):
    if re.match("^[0-9]+ *, *[0-9]+$", v):
        return map(int, v.split(","))
    raise argparse.ArgumentTypeError("String '%s' does not match required format" % (v,)) 

def _get_size_params_from_report(report):
    _fields = set(('scaled_hash','scaled_gray_hash','ahash','dhash_h','dhash_v'))
    return dict( (k, tuple(x[:2] for x in v)) for k,v in report.items() if k in _fields)
    
    
if __name__ == '__main__':
    import argparse
    # TODO: nice json flag
    parser = argparse.ArgumentParser(description='Create LSH testcases.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--output', '-o', default="-", help="The file to save the result to. Use '-' for stdout.")
    parser.add_argument('--fromtest', '-t', nargs='+', default=[], help="Create tests with the same parameter as in the given test files.")
    parser.add_argument('--fromurl', '-u', nargs='+', default=[], help="Create tests from given images (image url).")
    group_sizes = parser.add_argument_group(title='Sizes.', description='Sizes are looking like "WIDTH,HEIGHT".')
    group_sizes.add_argument('--sizeScale', '-s', nargs='+', type=SizeType, default=[], help="Size of scaled image.")
    group_sizes.add_argument('--sizeGray', '-g', nargs='+', type=SizeType, default=[], help="Size of scaled grayimage.")
    group_sizes.add_argument('--sizeAhash', '-a', nargs='+', type=SizeType, default=[], help="Size of ahash image.")
    group_sizes.add_argument('--sizeDhashH', '-d', nargs='+', type=SizeType, default=[], help="Size of dhash horizontal image.")
    group_sizes.add_argument('--sizeDhashV', '-v', nargs='+', type=SizeType, default=[], help="Size of dhash vertical image.")
    parser.add_argument('--name', '-n', default="LSH test", help="Name of the test.")
    parser.add_argument('--info', '-i', default="", help="Description of the test.")
    args = parser.parse_args()
    
    arg_params = {
              'scaled_hash': args.sizeScale,
              'scaled_gray_hash': args.sizeGray,
              'ahash': args.sizeAhash,
              'dhash_h': args.sizeDhashH,
              'dhash_v': args.sizeDhashV
              }
    
    # TODO: make version aware
    testcases = LSH_Testcase_v_0_1(args.name, args.info)
    for testcase in args.fromtest:
        with open(testcase, 'rb') as fp:
            testcase = json.load(fp)
        # TODO: error checks
        for test in testcase['tests']:
            params = _get_size_params_from_report(test)
            testcases.create_LSH_testcase_element(test['url'], test.get('name', ""), hash_sizes=params)
                 
        
    for url in args.fromurl:
        testcases.create_LSH_testcase_element(url, "", hash_sizes=arg_params)
    
    if args.output == '-':
        testcases.dump(sys.stdout, indent=2, sort_keys=True)
        exit(0)
    with open(args.output, 'wb') as fp:
        testcases.dump(fp, indent=2, sort_keys=True)