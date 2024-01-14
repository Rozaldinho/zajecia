import cv2
from flask import Flask
from flask_restful import Resource, Api


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

app = Flask(__name__)
api = Api(app)

class PeopleCounter(Resource):
    def get(self):

        image = cv2.imread('koncerty.jpg')
        image = cv2.resize(image, (700, 400))
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        return {'peopleCount': len(rects)}


api.add_resource(PeopleCounter, '/')
if __name__ == '__main__':
    app.run(debug=True, port=5001)
