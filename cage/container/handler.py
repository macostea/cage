import subprocess
import os
import re
import urllib.request
from docker import Client

# TODO: Check if Docker daemon is running. Start it if it's not.


class DockerNotInstalledError(Exception):
    pass


class ContainerHandler:
    def __init__(self, name, python_version):
        self.__name = name
        self.__python_version = python_version
        self.__client = Client(base_url='unix://var/run/docker.sock')
        self.__container = None

        self.__image_name = "cage/" + self.__name + self.__python_version

    @staticmethod
    def get_python_versions():
        # TODO: Download in a better place. Current dir does not seem like a good idea

        manifest_url = "https://raw.githubusercontent.com/docker-library/official-images/master/library/python"

        local_manifest_path = "manifest.txt"

        if not os.path.exists(local_manifest_path):
            response = urllib.request.urlopen(manifest_url)
            data = response.read()
            text = data.decode("utf-8")

            with open(local_manifest_path, "w") as manifest_file:
                manifest_file.write(text)

        versions = None

        with open(local_manifest_path, "r") as manifest_file:
            versions = ContainerHandler.__parse_manifest_file(manifest_file)

        return versions

    @staticmethod
    def __parse_manifest_file(manifest):
        regex = re.compile("^Directory: (?P<version>\d.\d)$")

        versions = []

        for line in manifest:
            match = regex.search(line)
            if match is not None:
                versions.append(match.group("version"))

        return versions

    @staticmethod
    def check_docker_installed():
        # TODO: Add check here
        pass

    def create_image(self):
        dockerfile_path = os.path.join("python", self.__python_version, "onbuild")
        response = self.__client.build(path=dockerfile_path, tag=self.__image_name, rm=True)
        res = [line for line in response]
        print(res)

    def start(self, command):
        self.__container = self.__client.create_container(self.__image_name, command=command)
        self.__client.start(self.__container)

        self.redirect_logs(self.__container)

    def redirect_logs(self, container):
        logs = self.__client.logs(container, stream=True)
        for line in logs:
            print(line)
