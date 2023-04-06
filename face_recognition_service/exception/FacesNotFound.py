
class FacesNotFound(BaseException):
    def __init__(self, message="No faces or multiple faces found"):
        self.message = message
        super().__init__(self.message)
