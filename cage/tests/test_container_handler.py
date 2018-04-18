import unittest
import os
import shutil
import threading
import requests
from cage.container import ContainerHandler


class TestContainerHandler(unittest.TestCase):
    def test_image_creation(self):
        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")
        test_cage_path = os.path.join(test_path, "test_cage")

        if not os.path.exists(test_cage_path):
            os.makedirs(test_cage_path)

        handler = ContainerHandler(test_cage_path, test_path)

        self.addCleanup(self.cleanup, test_path, test_cage_path, handler)

        if os.path.exists(os.path.join(test_path, "Dockerfile")):
            os.remove(os.path.join(test_path, "Dockerfile"))

        response = handler.create_image("3.5")

        response_list = [line for line in response]

        last_line = response_list[-1].decode("utf-8")
        self.assertTrue("Successfully" in last_line)

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
        handler.install_deps("requirements.txt")

        self.addCleanup(self.cleanup, test_path, test_cage_path, handler)

        # Make sure we have deps installed before starting the test
        handler.start("python --version")

        self.stop_thread = False

        t = threading.Thread(target=self.parallel_start, args=[handler, os.path.join(test_path, "ENV")])
        t.start()

        t.join(timeout=30)

        # Make sure we didn't time out
        self.assertFalse(t.is_alive())

        r = requests.get("http://localhost:5000/main")
        self.assertEqual(r.text, "This is a test app running in the Python cage")

    def test_python_versions(self):
        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")
        test_cage_path = os.path.join(test_path, "test_manifest_cage")

        handler = ContainerHandler(test_cage_path, test_path)

        self.addCleanup(self.cleanup, test_path, None, handler)

        versions = handler.get_python_versions()

        self.assertEqual(["2.7", "3.3", "3.4", "3.5", "3.6"], versions)

    def test_add_files(self):
        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")
        test_cage_path = os.path.join(test_path, "test_cage")

        if not os.path.exists(test_cage_path):
            os.makedirs(test_cage_path)

        handler = ContainerHandler(test_cage_path, test_path)

        self.addCleanup(self.cleanup, test_path, test_cage_path, handler)

        handler.create_image("3.5")

        # Single entry
        handler.add_files(".")
        found_count = 0

        with open(os.path.join(test_path, "Dockerfile"), "r") as dockerfile:
            for line in dockerfile:
                if line == "COPY . /usr/src/app\n":
                    found_count += 1

        self.assertEqual(found_count, 1)

        # Multiple entries should not be allowed
        handler.add_files(".")
        found_count = 0

        with open(os.path.join(test_path, "Dockerfile"), "r") as dockerfile:
            for line in dockerfile:
                if line == "COPY . /usr/src/app\n":
                    found_count += 1

        self.assertEqual(found_count, 1)

    def test_install_dependencies(self):
        test_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_app")
        test_cage_path = os.path.join(test_path, "test_cage")

        if not os.path.exists(test_cage_path):
            os.makedirs(test_cage_path)

        handler = ContainerHandler(test_cage_path, test_path)

        self.addCleanup(self.cleanup, test_path, test_cage_path, handler)

        handler.create_image("3.5")

        # Single entry
        handler.add_files(".")
        handler.install_deps("requirements.txt")
        found_count = 0

        with open(os.path.join(test_path, "Dockerfile"), "r") as dockerfile:
            for line in dockerfile:
                if line == "RUN pip install --no-cache-dir -r requirements.txt\n":
                    found_count += 1

        self.assertEqual(found_count, 1)

        # Multiple entries should not be allowed
        handler.install_deps("requirements.txt")
        found_count = 0

        with open(os.path.join(test_path, "Dockerfile"), "r") as dockerfile:
            for line in dockerfile:
                if line == "RUN pip install --no-cache-dir -r requirements.txt\n":
                    found_count += 1

        self.assertEqual(found_count, 1)

        # Bad file
        with self.assertRaises(FileNotFoundError):
            handler.install_deps("requirements")

    # UTILS
    def cleanup(self, test_path=None, test_cage_path=None, handler=None):
        # Cleanup

        self.stop_thread = True

        if test_path is not None and os.path.exists(os.path.join(test_path, "Dockerfile")):
            os.remove(os.path.join(test_path, "Dockerfile"))

        if test_cage_path is not None and os.path.exists(test_cage_path):
            shutil.rmtree(test_cage_path, ignore_errors=True)

        if handler is not None:
            handler.stop()

    def parallel_start(self, handler, envpath):
        response = handler.start("python main.py", envpath)

        for line in response:
            print(line)
            if line.decode("utf-8") == " * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)\n":
                break
            if self.stop_thread:
                break
