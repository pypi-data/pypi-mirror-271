import unittest
import PIL.Image
import torch
from irisml.tasks.create_ultralytics_val_transform import Task


class TestCreateUltralyticsValTransform(unittest.TestCase):
    def test_square(self):
        transform = Task(Task.Config(input_size=640, square=True)).execute(Task.Inputs()).transform

        image = PIL.Image.new('RGB', (100, 200))
        targets = torch.tensor([[0, 0.1, 0.1, 0.2, 0.2], [1, 0.3, 0.3, 0.4, 0.4]], dtype=torch.float32)

        new_image, new_targets = transform(image, targets)
        self.assertIsInstance(new_image, torch.Tensor)
        self.assertEqual(new_image.size(), (3, 640, 640))
        self.assertIsInstance(new_targets, torch.Tensor)
        self.assertEqual(new_targets.size(), (2, 5))

    def test_no_square(self):
        transform = Task(Task.Config(input_size=640, square=False)).execute(Task.Inputs()).transform

        image = PIL.Image.new('RGB', (100, 200))
        targets = torch.tensor([[0, 0.1, 0.1, 0.2, 0.2], [1, 0.3, 0.3, 0.4, 0.4]], dtype=torch.float32)

        new_image, new_targets = transform(image, targets)
        self.assertIsInstance(new_image, torch.Tensor)
        self.assertEqual(new_image.size(), (3, 640, 320))  # CHW
        self.assertIsInstance(new_targets, torch.Tensor)
        self.assertEqual(new_targets.size(), (2, 5))

        image = PIL.Image.new('RGB', (101, 200))
        new_image, new_targets = transform(image, targets)
        self.assertEqual(new_image.size(), (3, 640, 352))  # CHW
