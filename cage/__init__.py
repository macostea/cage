import argparse
import sys
import os
from cage.container import ContainerHandler
from cage.env import EnvHandler


def main():
    # TODO: Find a better way to organize the arguments
    parser = argparse.ArgumentParser(description="Develop and run your python application in clean Docker environments")
    parser.add_argument("command", help="the command you want to run", action="store")
    parser.add_argument("name", help="the full path to your cage", action="store")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-p", "--python", help="python version", action="store")
    parser.add_argument("-f", "--files", help="path to your app files to copy into the new cage", action="store")
    parser.add_argument("-s", "--script", help="the script you want to run", action="store")
    parser.add_argument("-r", "--requirements", help="path to the requirements file", action="store")
    args = parser.parse_args()

    command_list = args.command.split(":")

    # TODO: Add tests for this part as well
    if command_list[0] == "app":
        handle_container_command(command_list[1], args)

    ContainerHandler.check_docker_installed()


def handle_container_command(command, opts):
    supported_python_versions = ContainerHandler.get_python_versions()
    python_version = opts.python if opts.python is not None else ".".join(str(x) for x in sys.version_info[:2])

    assert python_version in supported_python_versions, "Selected python version {} is not in the supported list: {}".\
        format(python_version, supported_python_versions)

    if command == "create":
        # Create the new image
        container_handler = ContainerHandler(opts.name, os.getcwd())

        if not os.path.exists(opts.name):
            os.makedirs(opts.name)

        res = container_handler.create_image(python_version)
        for line in res:
            print(line)

        # Copy the binaries
        env_handler = EnvHandler(os.path.join(os.path.dirname(os.path.realpath(__file__)), "env", "scripts"))
        env_handler.init_env(opts.name)

    elif command == "addfiles":
        container_handler = ContainerHandler(opts.name, os.getcwd())

        container_handler.add_files(opts.files)

    elif command == "run":
        container_handler = ContainerHandler(opts.name, os.getcwd())

        result = container_handler.start(opts.script)
        for line in result:
            print(line)

    elif command == "deps":
        container_handler = ContainerHandler(opts.name, os.getcwd())

        container_handler.install_deps(opts.requirements)
