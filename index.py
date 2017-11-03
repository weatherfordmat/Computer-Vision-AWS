from pyimagesearch.panorama import Stitcher
import logging
from flask import Flask
from flask import jsonify, request
import urllib.request
import json
import numpy as np
import requests
import imutils
import base64
import cv2
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

app = Flask(__name__)

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def url_to_image(path):
	if path[0:4] == 'http' or path[0:4] == 'data':
		resp = urllib.request.urlopen(path, context=ctx)
		image = np.asarray(bytearray(resp.read()), dtype="uint8")
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		return image
	else:
		convert = base64.b64decode(path)
		l = np.asarray(bytearray(convert), dtype="uint8")
		image = cv2.imdecode(l, cv2.IMREAD_COLOR)
		return image

def combineImages(a, b):
	imageA = url_to_image(a)
	imageB = url_to_image(b)
	gA = imutils.resize(imageA, width=350)
	gB = imutils.resize(imageB, width=350)

	stitcher = Stitcher()
	(result, vis) = stitcher.stitch([gA, gB], showMatches=True)

	r = cv2.imencode('.jpg', result)[1]
	r = base64.b64encode(r).decode("utf-8")
	return r

def getText(content):
	payload = {
		"requests": [{
			"image": {
				"content": content
			},
			"features": [
				{
					"type": "TEXT_DETECTION"
				}
			]
			}
		]
	}
	para = { "key": HIDDEN } 
	gcloud = 'https://vision.googleapis.com/v1/images:annotate?key=HIDDEN'

	# make request
	res = requests.post(gcloud, params=para, json=payload, headers={'Content-Type': 'application/json' })
        return res.text

@app.route('/', methods=['GET', 'POST'])
def handler(event=None, context=None):
	logger.info('Lambda function invoked handler()')
	with app.app_context():
		if request.method == 'GET':
			logger.info('Lambda function invoked GET')
			return jsonify({"message": "We kindly request a POST method with two images (firstImage and secondImage) sent in the body. N. B. They must be encoded as base64."})
		else:
			data = json.loads(request.data)
			logger.info('Lambda function invoked POST')
			r = combineImages(data["firstImage"], data["secondImage"])
			return getText(r)

if __name__ == '__main__':
    app.run(debug=True)
