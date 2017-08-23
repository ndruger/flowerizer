import sys, argparse, math, cv2, os
import numpy as np
from scipy.io import loadmat

targets = [
  {
    'name': 'water lilies',
    'category': 73,
    'paing_color_bgr': [0, 0xff, 0],
  },
  {
    'name': 'rose',
    'category': 74,
    'paing_color_bgr': [0, 0, 0xff],
  },
  {
    'name': 'sunflower',
    'category': 54,
    'paing_color_bgr': [0, 0xff, 0xff],
  },
]

TEST_COUNT = 5;
ORIG_IMG_PATH = './pix2pix_train_data/orig/jpg'
ORIG_SEG_PATH = './pix2pix_train_data/orig/segmim'

OUT_TRAIN_PATH = './pix2pix_train_data/train'
OUT_TEST_PATH = './pix2pix_train_data/test'
OUT_VAL_PATH = './pix2pix_train_data/val'

for d in [OUT_TRAIN_PATH, OUT_TEST_PATH, OUT_VAL_PATH]:
  os.makedirs(d, exist_ok=True)

def image_ids_in_category(category):
  mat = loadmat('./pix2pix_train_data/orig/imagelabels.mat')
  labels = mat['labels'][0]
  found = []
  for i in range(0, len(labels)):
    if labels[i] == category:
      found.append(i + 1) # to 1 base filename
  return found

def padded_id(id):
  return '{:05d}'.format(id)

def orig_img_name(id):
  return "image_{}.jpg".format(padded_id(id))

def orig_seg_name(id):
  return "segmim_{}.jpg".format(padded_id(id))

def out_name(id):
  return "image_{}.png".format(padded_id(id))

def paint(img, color_bgr):
  for x in range(0, 256):
    for y in range(0, 256):
      px = img[x, y] # b, g, r
      d = math.sqrt((255 - px[0]) ** 2 + (0 - px[1]) ** 2 + (0 - px[2]) ** 2)
      if d > 10:
        img[x, y] = color_bgr
  return img

def translate(id, paing_color_bgr, is_train):
  print("translating id={0}, is_train={1}".format(id, is_train))
  img = cv2.imread(os.path.join(ORIG_IMG_PATH, orig_img_name(id)))
  seg = cv2.imread(os.path.join(ORIG_SEG_PATH, orig_seg_name(id)))
  resized_img = cv2.resize(img, (256, 256))
  resized_seg = cv2.resize(seg, (256, 256))
  painted_seg = paint(resized_seg, paing_color_bgr)
  joined = np.hstack((resized_img, painted_seg))
  if is_train:
    cv2.imwrite(os.path.join(OUT_TRAIN_PATH, out_name(id)), joined)
  else:
    cv2.imwrite(os.path.join(OUT_TEST_PATH, out_name(id)), joined)
    cv2.imwrite(os.path.join(OUT_VAL_PATH, out_name(id)), painted_seg)

for target in targets:
  ids = image_ids_in_category(target['category'])
  test_ids = ids[-TEST_COUNT:]
  train_ids = ids[:-TEST_COUNT]
  for id in train_ids:
    translate(id, target['paing_color_bgr'], True)
  for id in test_ids:
    translate(id, target['paing_color_bgr'], False)

