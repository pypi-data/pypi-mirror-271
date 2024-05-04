# Copyright (c) 2024 Philipp Rouast
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from prpy.numpy.image import crop_slice_resize

import numpy as np
import pytest
import tensorflow as tf

@pytest.mark.parametrize("target_size", [6, 3, (6, 12)])
@pytest.mark.parametrize("n_frames", [None, 3])
@pytest.mark.parametrize("roi", [(2, 2, 7, 7), [2, 2, 7, 7], None])
@pytest.mark.parametrize("target_idxs", [None, [0, 2], (0, 2), np.asarray([0, 2])])
@pytest.mark.parametrize("preserve_aspect_ratio", [True, False])
@pytest.mark.parametrize("library", ["cv2", "tf", "PIL"]) # TODO: Test prpy
@pytest.mark.parametrize("scale_algorithm", ["bicubic", "area", "lanczos", "bilinear"]) # TODO: Test box
@pytest.mark.parametrize("keepdims", [True, False])
def test_crop_slice_resize(target_size, n_frames, roi, target_idxs, preserve_aspect_ratio, library, scale_algorithm, keepdims):
  if (n_frames is None and target_idxs is not None) or \
     (library == "PIL" and scale_algorithm == "area"):
    pytest.skip("Skip because parameter combination does not work")
  if n_frames is None:
    images_in = np.random.uniform(size=(8, 12, 3), low=0, high=255)
  else:
    images_in = np.random.uniform(size=(n_frames, 8, 12, 3), low=0, high=255)
  images_in = images_in.astype(np.uint8)
  images_out = crop_slice_resize(
    inputs=images_in, target_size=target_size, roi=roi, target_idxs=target_idxs,
    library=library, preserve_aspect_ratio=preserve_aspect_ratio,
    keepdims=keepdims, scale_algorithm=scale_algorithm)
  expected_frames = len(target_idxs) if target_idxs is not None else n_frames
  if expected_frames == 1 or expected_frames is None:
    expected_frames = 1 if keepdims else None
  if isinstance(target_size, int):
    if preserve_aspect_ratio is True and roi is None:
      expected_shape = (int(target_size*8./12), target_size, 3)
    else:
      expected_shape = (target_size, target_size, 3)
  else:
    if preserve_aspect_ratio is True and roi is None:
      expected_shape = (target_size[0], int(target_size[0]*12./8), 3)
    elif preserve_aspect_ratio is True and roi is not None:
      expected_shape = (target_size[0], target_size[0], 3)
    else:
      expected_shape = (target_size[0], target_size[1], 3)
  expected_shape = (expected_frames,) + expected_shape if expected_frames is not None else expected_shape
  assert images_out.shape == expected_shape
  if library == 'tf':
    assert tf.is_tensor(images_out)
  else:
    assert isinstance(images_out, np.ndarray)

def test_crop_slice_resize_retinaface():
  images_in = np.random.uniform(size=(480, 640, 3), low=0, high=255)  
  images_in = images_in.astype(np.uint8)
  images_out = crop_slice_resize(
    inputs=images_in, target_size=224, roi=(0, 0, 480, 640), target_idxs=None,
    library='tf', preserve_aspect_ratio=True, keepdims=True, scale_algorithm='bicubic')
  assert images_out.shape == (1, 224, 224, 3)
