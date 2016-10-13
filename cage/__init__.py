import argparse
import sys
from cage.container import ContainerHandler


def main():
    parser = argparse.ArgumentParser(description="Develop and run your python application in clean Docker environments")
    parser.add_argument("name", help="the name of the cage you want to create")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-p", "--python", help="python version", action="store")
    args = parser.parse_args()

    ContainerHandler.check_docker_installed()

    supported_python_versions = ContainerHandler.get_python_versions()
    python_version = args.python if args.python is not None else ".".join(str(x) for x in sys.version_info[:2])

    assert python_version in supported_python_versions, "Selected python version {} is not in the supported list: {}".\
        format(python_version, supported_python_versions)

    handler = ContainerHandler(args.name, python_version)
    handler.create_image()
