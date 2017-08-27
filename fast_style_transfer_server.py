import sys
sys.path.append('./fast-style-transfer/src')
import transform
import numpy as np, vgg, pdb, os, cv2, argparse
import tensorflow as tf

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver

parser = argparse.ArgumentParser()
parser.add_argument('--model_file', required=True)
parser.add_argument('--port', default=8080, type=int)
args = parser.parse_args()

img_shape = (256, 256, 3)

batch_size = 1
soft_config = tf.ConfigProto(allow_soft_placement=True)
soft_config.gpu_options.allow_growth = True

sess = tf.Session(config=soft_config)
global batch_shape
batch_shape = (batch_size,) + img_shape
img_placeholder = tf.placeholder(tf.float32, shape=batch_shape, name='img_placeholder')
global preds
preds = transform.net(img_placeholder)

saver = tf.train.Saver()
saver.restore(sess, args.model_file)

def restore_color(img_for_y, img_for_uv):
    y, _, _ = cv2.split(cv2.cvtColor(img_for_y, cv2.COLOR_BGR2YUV))
    _, u, v = cv2.split(cv2.cvtColor(img_for_uv, cv2.COLOR_BGR2YUV))
    yuv_img = cv2.merge((y, u, v))
    bgr_img = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)
    return bgr_img

def translate(bgr_img):
    rbg_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    x = np.zeros(batch_shape, dtype=np.float32)
    x[0] = rbg_img
    y = sess.run(preds, feed_dict={img_placeholder:x})
    out_rgb_img = np.clip(y[0], 0, 255).astype(np.uint8)
    out_bgr_img = cv2.cvtColor(out_rgb_img, cv2.COLOR_RGB2BGR)
    color_restored = restore_color(out_bgr_img, bgr_img)
    return color_restored

class Handler(BaseHTTPRequestHandler):
    def set_cors(self):
        self.send_header("access-control-allow-origin", "*")
        allow_headers = self.headers.get("access-control-request-headers", "*")
        self.send_header("access-control-allow-headers", allow_headers)
        self.send_header("access-control-allow-methods", "POST, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(200)
        self.set_cors();

    def do_POST(self):
        print("post!!")
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        bgr_img = cv2.imdecode(np.fromstring(data_string, dtype=np.uint8), 1)
        translated = translate(bgr_img)
        self.send_response(200)
        self.send_header('Content-type', 'image/png')
        self.set_cors();
        self.end_headers()
        self.wfile.write(cv2.imencode('.png', translated)[1].tostring())
        return

def run(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, Handler)
    httpd.serve_forever()
    print('httpd running...')
    sys.stdout.flush()

run(args.port)
