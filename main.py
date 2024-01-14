import cv2
from flask import Flask, request
from flask_restful import Resource, Api
import shutil
import requests

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)

class PeopleCounterStatic(Resource):

    def get(self):

        image = cv2.imread('koncerty.jpg')
        image = cv2.resize(image, (700, 400))
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        return {'peopleCount': len(rects)}


class PeopleCounterDynamicUrl(Resource):

    def get(self):
        url = request.args.get('url')
        print('url',url)

        res = requests.get(url, stream = True)
        file_name = 'download-images-python.jpg'
        if res.status_code == 200:
            with open(file_name,'wb') as f:
                 shutil.copyfileobj(res.raw, f)
            print('Image sucessfully Downloaded: ',file_name)
        else:
            print('Image Couldn\'t be retrieved')

        image = cv2.imread('koncerty.jpg')
        image = cv2.resize(image, (700, 400))
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)


        return {'peopleCount': len(rects)}


api.add_resource(PeopleCounterStatic, '/')
api.add_resource(PeopleCounterDynamicUrl, '/dynamic')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
