import unittest
import os
from cage.container import ContainerHandler


class TestContainerHandler(unittest.TestCase):
    def test_image_creation(self):
        handler = ContainerHandler("test_cage", "3.5")

        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")

        if os.path.exists(os.path.join(test_path, "Dockerfile")):
            os.remove(os.path.join(test_path, "Dockerfile"))

        response = handler.create_image(test_path)

        for line in response:
            print(line)

        last_line = response[-1].decode("utf-8")
        self.assertTrue("Successfully built" in last_line)

    def test_container_start(self):
        handler = ContainerHandler("test_cage", "3.5")

        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")

        if os.path.exists(os.path.join(test_path, "Dockerfile")):
            os.remove(os.path.join(test_path, "Dockerfile"))

        handler.create_image(test_path)

        response = handler.start("python main.py")

        last_line = None

        for line in response:
            last_line = line

        self.assertEqual(last_line.decode("utf-8"), "This is a test app running in the Python cage\n")
