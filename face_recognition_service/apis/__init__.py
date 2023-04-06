from flask_restx import Api

from .face_recognition_api import api as face_recognition_api

api = Api(
    title='Face Recognition Service API',
    version='1.0'
)

api.add_namespace(face_recognition_api)
