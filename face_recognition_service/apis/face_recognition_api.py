import werkzeug
from flask import jsonify
from flask_restx import Namespace, Resource, fields, reqparse
import logging
import numpy as np
import cv2

from core.face_recognition_service import FaceRecognitionService
from exception.FacesNotFound import FacesNotFound

api = Namespace('api/face-recognition', description='Face recognition related operations')

# Initialize dependencies
face_recognition_service = FaceRecognitionService()

# Set up logging
logger = logging.getLogger(__name__)

# Define a request parser for file uploads
image_parser = reqparse.RequestParser()
image_parser.add_argument('image',
                          type=werkzeug.datastructures.FileStorage,
                          location='files',
                          required=True,
                          help='Image file')

image_list_parser = reqparse.RequestParser()
image_list_parser.add_argument('images',
                               type=werkzeug.datastructures.FileStorage,
                               location='files',
                               required=True,
                               action='append',
                               help='List of images.')

feature_model = api.model('Feature', {
    'value': fields.Float,
    'type': fields.String(attribute=lambda x: x.type.value, description='Type of feature')
})


@api.route('/image')
class SingleImageUpload(Resource):
    @api.response(200, 'Success', feature_model, as_list=True)
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    @api.expect(image_parser)  # Attach the file upload parser to the endpoint
    def post(self):

        args = image_parser.parse_args()  # Parse the incoming request

        # Retrieve the image from the request
        image_file = args['image']

        # Validate the image file format
        if not image_file or not werkzeug.utils.secure_filename(image_file.filename):
            return {"error": "Invalid image format"}, 400

        try:
            # Read the image data and convert it to a numpy array
            image_data = np.frombuffer(image_file.read(), np.uint8)
            # Decode the numpy array as an image using OpenCV

            image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
            return face_recognition_service.extract_features(image), 200
        except FacesNotFound as e:
            return {"error": str(e.message)}, 400
        except Exception as e:
            return {"error": str(e)}, 500


@api.route('/images')
class MultipleImagesUpload(Resource):
    @api.response(200, 'Success', feature_model, as_list=True)
    @api.response(400, 'Bad Request')
    @api.response(500, 'Internal Server Error')
    @api.expect(image_list_parser)
    def post(self):
        args = image_list_parser.parse_args()
        image_files = args['images']

        for image_file in image_files:
            if not image_file or not werkzeug.utils.secure_filename(image_file.filename):
                return {"error": "Invalid image format"}, 400

        try:
            images = []
            for image_file in image_files:
                image_data = np.frombuffer(image_file.read(), np.uint8)
                image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
                images.append(image)
            features = face_recognition_service.extract_mean_features(images)
            return features, 200
        except FacesNotFound as e:
            return {"error": str(e.message)}, 400  # Use a colon (:) instead of a comma (,)
        except Exception as e:
            return {"error": str(e)}, 500


