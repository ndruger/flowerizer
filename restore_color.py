import cv2, argparse

parser = argparse.ArgumentParser()
parser.add_argument('--y_file', required=True)
parser.add_argument('--uv_file', required=True)
parser.add_argument('--out_file', required=True)
args = parser.parse_args()

img_for_y = cv2.imread(args.y_file)
img_for_uv = cv2.imread(args.uv_file)

y, _, _ = cv2.split(cv2.cvtColor(img_for_y, cv2.COLOR_BGR2YUV))
_, u, v = cv2.split(cv2.cvtColor(img_for_uv, cv2.COLOR_BGR2YUV))
yuv_img = cv2.merge((y, u, v))
bgr_img = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)

cv2.imwrite(args.out_file, bgr_img)
