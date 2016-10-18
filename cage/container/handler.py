import os
import re
import urllib.request
from docker import Client

# TODO: Check if Docker daemon is running. Start it if it's not.


class DockerNotInstalledError(Exception):
    pass


class ContainerHandler:
    def __init__(self, cage_path, app_path):
        self.__path = cage_path
        self.__app_path = app_path
        self.__name = os.path.basename(os.path.normpath(cage_path))
        self.__client = Client(base_url='unix://var/run/docker.sock')

        self.__container = None

        self.__image_name = "cage/" + self.__name

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

    def create_image(self, python_version=None):
        if python_version is not None and not os.path.exists(os.path.join(self.__app_path, "Dockerfile")):
            dockerfile_content = "FROM python:{}\n" \
                                 "RUN mkdir -p /usr/src/app\n" \
                                 "WORKDIR /usr/src/app\n" \
                .format(python_version)
            with open(os.path.join(self.__app_path, "Dockerfile"), "w") as dockerfile:
                dockerfile.write(dockerfile_content)

        response = self.__client.build(path=self.__app_path, tag=self.__image_name, rm=True)

        return response

    def start(self, command):
        res = self.create_image()
        for line in res:
            print(line)
        container = self.__client.create_container(self.__image_name, command=command)
        self.__client.start(container)

        return self.redirect_logs(container)

    def add_files(self, path):
        self.__write_to_dockerfile("COPY {} /usr/src/app".format(path))

    def install_deps(self, requirements_file):
        self.__write_to_dockerfile("RUN pip install --no-cache-dir -r {}".format(requirements_file))

    def redirect_logs(self, container):
        logs = self.__client.logs(container, stream=True)
        return logs

    def __write_to_dockerfile(self, line):
        with open(os.path.join(self.__app_path, "Dockerfile"), "r") as dockerfile:
            dockerfile.seek(0)
            line_exists = line in dockerfile.read()

        if not line_exists:
            with open(os.path.join(self.__app_path, "Dockerfile"), "a") as dockerfile:
                dockerfile.write(line)
                dockerfile.write("\n")
