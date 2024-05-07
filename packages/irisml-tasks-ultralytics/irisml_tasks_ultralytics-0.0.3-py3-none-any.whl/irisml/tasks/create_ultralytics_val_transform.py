import dataclasses
import typing
import numpy
import PIL.Image
import torch
import ultralytics.data.augment
import ultralytics.utils.instance
import irisml.core


class Task(irisml.core.TaskBase):
    """Create a transform function for prediction using Ultralytics library.

    Config:
        input_size (int): The max size of the longer side of the image.
        square (bool): If True, the image will be padded to be square. If False, the aspect ratio will be almost preserved. Default is True.
    """

    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Config:
        input_size: int
        square: bool = True

    @dataclasses.dataclass
    class Outputs:
        transform: typing.Callable

    def execute(self, inputs):
        return self.Outputs(UltralyticsTransform(self.config.input_size, self.config.square))

    def dry_run(self, inputs):
        return self.execute(inputs)


class UltralyticsTransform:
    def __init__(self, input_size, square):
        self._transform = ultralytics.data.augment.LetterBox(new_shape=(input_size, input_size), auto=not square)

    def __call__(self, inputs, targets):
        assert isinstance(inputs, PIL.Image.Image)
        assert isinstance(targets, torch.Tensor) and targets.dim() == 2 and targets.size(1) == 5

        bboxes = targets[:, 1:]

        # No idea why segments is needed. It'll throw an error if it's not passed.
        instances = ultralytics.utils.instance.Instances(bboxes=numpy.array(bboxes), bbox_format='xyxy', segments=numpy.zeros((0, 1000, 2), dtype=numpy.float32))
        # Ultralytics expects the image to be in HWC, [0, 255]
        image = numpy.array(inputs)
        labels = {'img': image, 'cls': numpy.array(targets[:, 0]), 'instances': instances}
        new_labels = self._transform(labels)

        # convert from numpy HWC [0, 255] to torch CHW [0, 1]
        new_image = torch.from_numpy(new_labels['img'].transpose(2, 0, 1)).float() / 255.0

        new_labels['instances'].normalize(new_image.size(2), new_image.size(1))
        # We have to access the private member to convert the bbox format :(
        new_bboxes = new_labels['instances']._bboxes
        new_bboxes.convert('xyxy')
        new_bboxes = torch.from_numpy(new_bboxes.bboxes)

        new_targets = torch.cat([torch.from_numpy(new_labels['cls']).unsqueeze(1), new_bboxes], dim=1)

        return new_image, new_targets
