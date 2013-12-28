from tester import *

from PIL import Image, EpsImagePlugin
import sys

if EpsImagePlugin.gs_windows_binary == False:
    # already checked. Not there. 
    skip()
    
if not sys.platform.startswith('win'):
    import subprocess
    try:
        gs = subprocess.Popen(['gs','--version'], stdout=subprocess.PIPE)
        gs.stdout.read()
    except OSError:
        # no ghostscript
        skip()

#Our two EPS test files (they are identical except for their bounding boxes)
file1 = "Tests/images/zero_bb.eps"
file2 = "Tests/images/non_zero_bb.eps"

#Due to palletization, we'll need to convert these to RGB after load
file1_compare = "Tests/images/zero_bb.png"
file1_compare_scale2 = "Tests/images/zero_bb_scale2.png"

file2_compare = "Tests/images/non_zero_bb.png"
file2_compare_scale2 = "Tests/images/non_zero_bb_scale2.png"

def test_sanity():
    #Regular scale
    image1 = Image.open(file1)
    try:
        image1.load()
    except OSError:
        #Tests/test_file_eps.py:19: image1.load() failed:
        #Traceback (most recent call last):
        #  File "Tests/test_file_eps.py", line 19, in test_sanity
        #    image1.load()
        #  File "/Users/aclark/Developer/Pillow/PIL/EpsImagePlugin.py", line 318, in load
        #    self.im = Ghostscript(self.tile, self.size, self.fp, scale)
        #  File "/Users/aclark/Developer/Pillow/PIL/EpsImagePlugin.py", line 89, in Ghostscript
        #    gs = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        #  File "/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 709, in __init__
        #    errread, errwrite)
        #  File "/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/lib/python2.7/subprocess.py", line 1326, in _execute_child
        #    raise child_exception
        #OSError: [Errno 2] No such file or directory
        skip("Image load failed, missing Ghostscript?")
    assert_equal(image1.mode, "RGB")
    assert_equal(image1.size, (460, 352))
    assert_equal(image1.format, "EPS")

    image2 = Image.open(file2)
    image2.load()
    assert_equal(image2.mode, "RGB")
    assert_equal(image2.size, (360, 252))
    assert_equal(image2.format, "EPS")

    #Double scale
    image1_scale2 = Image.open(file1)
    image1_scale2.load(scale=2)
    assert_equal(image1_scale2.mode, "RGB")
    assert_equal(image1_scale2.size, (920, 704))
    assert_equal(image1_scale2.format, "EPS")

    image2_scale2 = Image.open(file2)
    image2_scale2.load(scale=2)
    assert_equal(image2_scale2.mode, "RGB")
    assert_equal(image2_scale2.size, (720, 504))
    assert_equal(image2_scale2.format, "EPS")

def test_render_scale1():
    #We need png support for these render test
    codecs = dir(Image.core)
    if "zip_encoder" not in codecs or "zip_decoder" not in codecs:
        skip("zip/deflate support not available")

    #Zero bounding box
    image1_scale1 = Image.open(file1)
    image1_scale1.load()
    image1_scale1_compare = Image.open(file1_compare).convert("RGB")
    image1_scale1_compare.load()
    assert_image_similar(image1_scale1, image1_scale1_compare, 5)

    #Non-Zero bounding box
    image2_scale1 = Image.open(file2)
    image2_scale1.load()
    image2_scale1_compare = Image.open(file2_compare).convert("RGB")
    image2_scale1_compare.load()
    assert_image_similar(image2_scale1, image2_scale1_compare, 10)

def test_render_scale2():
    #We need png support for these render test
    codecs = dir(Image.core)
    if "zip_encoder" not in codecs or "zip_decoder" not in codecs:
        skip("zip/deflate support not available")

    #Zero bounding box
    image1_scale2 = Image.open(file1)
    image1_scale2.load(scale=2)
    image1_scale2_compare = Image.open(file1_compare_scale2).convert("RGB")
    image1_scale2_compare.load()
    assert_image_similar(image1_scale2, image1_scale2_compare, 5)

    #Non-Zero bounding box
    image2_scale2 = Image.open(file2)
    image2_scale2.load(scale=2)
    image2_scale2_compare = Image.open(file2_compare_scale2).convert("RGB")
    image2_scale2_compare.load()
    assert_image_similar(image2_scale2, image2_scale2_compare, 10)

