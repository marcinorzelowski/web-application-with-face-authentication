from enum import Enum

from utils import image_utils


class HaarFeatureType(Enum):
    EDGE_HORIZONTAL = 1
    EDGE_VERTICAL = 2
    LINE_HORIZONTAL = 3
    LINE_VERTICAL = 4
    FOUR_SQUARED = 5


class HaarFeature:

    def __init__(self, x, y, width, height, type):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.type = type
        self.value = 0

    def __str__(self):
        return f"HaarFeature(x={self.x}, y={self.y}, width={self.width}, height={self.height}, type={self.type.name}, value={self.value})"

    def __repr__(self):
        return self.__str__()

    def calculate_value(self, integral_image):
        white, black = 0, 0
        if self.type == HaarFeatureType.LINE_HORIZONTAL:
            white += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=self.y, x2=self.x + self.width - 1,
                                                       y2=int(self.y + self.height / 3) - 1)
            black += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=int(self.y + self.height / 3),
                                                       x2=self.x + self.width - 1,
                                                       y2=int(self.y + 2 * self.height / 3) - 1)
            white += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=int(self.y + 2 * self.height / 3),
                                                       x2=self.x + self.width - 1, y2=self.y + self.height - 1)
        if self.type == HaarFeatureType.LINE_VERTICAL:
            white += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=self.y,
                                                       x2=int(self.x + self.width / 3 - 1),
                                                       y2=self.y + self.height - 1)
            black += image_utils.calculate_summed_area(integral_image, x1=int(self.x + self.width / 3), y1=self.y,
                                                       x2=int(self.x + 2 * self.width / 3 - 1),
                                                       y2=self.y + self.height - 1)
            white += image_utils.calculate_summed_area(integral_image, x1=int(self.x + 2 * self.width / 3),
                                                       y1=int(self.y),
                                                       x2=self.x + self.width - 1, y2=self.y + self.height - 1)
        if self.type == HaarFeatureType.EDGE_HORIZONTAL:
            white += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=self.y,
                                                       x2=self.x + self.width - 1, y2=int(self.y + self.height/2 - 1))
            black += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=int(self.y + self.height / 2),
                                                       x2=self.x + self.width - 1, y2=int(self.y + self.height - 1))
        if self.type == HaarFeatureType.EDGE_VERTICAL:
            white += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=self.y,
                                                       x2=int(self.x + self.width / 2 - 1), y2=int(self.y + self.height - 1))
            black += image_utils.calculate_summed_area(integral_image, x1=int(self.x + self.width / 2), y1=self.y,
                                                       x2=self.x + self.width - 1, y2=int(self.y + self.height - 1))
        if self.type == HaarFeatureType.FOUR_SQUARED:
            white += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=self.y,
                                                       x2=int(self.x + self.width / 2 - 1), y2=int(self.y + self.height / 2 - 1))
            white += image_utils.calculate_summed_area(integral_image, x1=int(self.x + self.width / 2), y1=int(self.y + self.height / 2),
                                                       x2=int(self.x + self.width - 1), y2=self.y + self.height - 1)
            black += image_utils.calculate_summed_area(integral_image, x1=self.x, y1=self.y,
                                                       x2=self.x + self.width - 1, y2=self.y + self.height - 1) - white
        return white - black
