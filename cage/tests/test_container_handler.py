import unittest
import os
from cage.container import ContainerHandler


class TestContainerHandler(unittest.TestCase):
    def test_image_creation(self):
        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")
        test_cage_path = os.path.join(test_path, "test_cage")

        if not os.path.exists(test_cage_path):
            os.makedirs(test_cage_path)

        handler = ContainerHandler(test_cage_path, test_path)

        if os.path.exists(os.path.join(test_path, "Dockerfile")):
            os.remove(os.path.join(test_path, "Dockerfile"))

        response = handler.create_image("3.5")

        response_list = [line for line in response]

        last_line = response_list[-1].decode("utf-8")
        self.assertTrue("Successfully built" in last_line)

    def test_container_start(self):
        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")
        test_cage_path = os.path.join(test_path, "test_cage")

        if not os.path.exists(test_cage_path):
            os.makedirs(test_cage_path)

        handler = ContainerHandler(test_cage_path, test_path)

        if os.path.exists(os.path.join(test_path, "Dockerfile")):
            os.remove(os.path.join(test_path, "Dockerfile"))

        handler.create_image("3.5")
        handler.add_files(".")

        response = handler.start("python main.py")

        last_line = None

        for line in response:
            last_line = line

        self.assertEqual(last_line.decode("utf-8"), "This is a test app running in the Python cage\n")
