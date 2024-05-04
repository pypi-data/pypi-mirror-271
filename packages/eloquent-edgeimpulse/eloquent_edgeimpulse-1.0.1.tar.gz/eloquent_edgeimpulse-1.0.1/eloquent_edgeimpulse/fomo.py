import numpy as np
from eloquent_edgeimpulse.runner import ImpulseRunner


class Fomo:
    """
    Wrapper for EI FOMO model
    """
    def __init__(self, model_path: str):
        """

        :param model_path:
        """
        self.runner = ImpulseRunner(model_path)
        self.model_info = self.runner.init()
        self.model_params = self.model_info['model_parameters']
        self.results = []

        assert self.model_params['model_type'] == 'constrained_object_detection', 'model type *must* be "constrained_object_detection"'

    @property
    def width(self) -> int:
        """
        Get input image width
        :return:
        """
        return self.model_params['image_input_width']

    @property
    def height(self) -> int:
        """
        Get input image height
        :return:
        """
        return self.model_params['image_input_height']

    @property
    def depth(self) -> int:
        """
        Get input image number of channels
        :return:
        """
        return self.model_params['image_channel_count']

    @property
    def shape(self) -> tuple:
        """
        Get input shape
        :return:
        """
        return (self.height, self.width, self.depth)

    @property
    def bboxes(self) -> list:
        """
        Return list of detected bboxes
        :return:
        """
        return [
            {**bbox, **{
                'cx': bbox['x'] + bbox['width'] // 2,
                'cy': bbox['y'] + bbox['height'] // 2,
                'score': bbox['value']
            }}
            for bbox in self.results['result']['bounding_boxes']
        ]

    def detect(self, image) -> list:
        """
        Detect objects in image
        :param image:
        :return:
        """
        # convert PIL image to numpy
        if image.__class__.__name__ == 'Image':
            image = np.asarray(image)
            
        height, width = image.shape[:2]

        assert width == self.width, f'image width *must* be {self.width}'
        assert height == self.height, f'image height *must* be {self.height}'

        # convert from float [0, 1] to int [0, 255]
        if image.min() >= 0 and image.max() <= 1:
            image = (image * 255).astype(int)

        # convert 2D image to 3D image (RGB)
        if len(image.shape) == 2 or image.shape[2] == 1:
            gray = image.reshape(image.shape[:2])
            image = np.dstack((gray, gray, gray))

        # convert 3D uint8 to 1D uint24
        def to_uint24(pixel):
            return (pixel[0] << 16) | (pixel[1] << 8) | pixel[2]

        image = [to_uint24(rgb) for rgb in image.astype(int).reshape((self.width * self.height, 3))]
        # force int dtype
        image = np.asarray(image, dtype=int).tolist()
        self.results = self.runner.classify(image)

        return self.bboxes

