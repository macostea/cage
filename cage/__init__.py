import argparse
from cage.container import ContainerHandler


def main():
    parser = argparse.ArgumentParser(description="Develop and run your python application in clean Docker environments")
    parser.add_argument("name", help="the name of the cage you want to create")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-p", "--python", help="python version", action="store")
    args = parser.parse_args()

    ContainerHandler.get_python_versions()
    # TODO: Check if passed Python version is supported

    handler = ContainerHandler(args.name, args.python)
    handler.create_image()
