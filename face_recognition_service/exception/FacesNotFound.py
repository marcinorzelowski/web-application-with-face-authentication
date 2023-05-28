
class FacesNotFound(BaseException):
    def __init__(self, message="Na przesłanym zdjęciu nie wykryto twarzy. Upewnij się, że na przesłanym zdjęciu jest widoczna twarz i spróbuj ponownie."):
        self.message = message
        super().__init__(self.message)
