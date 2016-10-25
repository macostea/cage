import os
import re
import urllib.request
import pickle
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

        self.__container = self.__get_container()

        self.__image_name = "cage/" + self.__name

    def get_python_versions(self):
        # TODO: Download in a better place. Current dir does not seem like a good idea

        manifest_url = "https://raw.githubusercontent.com/docker-library/official-images/master/library/python"

        local_manifest_path = os.path.join(self.__path, "manifest.txt")

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

    def start(self, command, env=None):
        res = self.create_image()
        for line in res:
            print(line)

        regex = re.compile("^PORT=(?P<port>\d+$)")
        ports = []
        env_list = []

        if env is not None:
            with open(env, "r") as env_file:
                for line in env_file:
                    # Add env line to env list
                    env_list.append(line.rstrip("\n"))

                    # Check if PORT is defined in the env file
                    match = regex.search(line)
                    if match is not None:
                        ports.append(int(match.group("port")))

        host_config = self.__client.create_host_config(port_bindings=dict(zip(ports, ports)))

        container = self.__client.create_container(self.__image_name, command=command, ports=ports,
                                                   host_config=host_config, environment=env_list)
        self.__set_container(container)

        self.__client.start(self.__container)

        return self.redirect_logs(self.__container)

    def stop(self):
        if self.__container is not None:
            self.__client.stop(self.__container)

    def add_files(self, path):
        self.__write_to_dockerfile("COPY {} /usr/src/app".format(path))

    def install_deps(self, requirements_file):
        if os.path.exists(requirements_file):
            self.__write_to_dockerfile("RUN pip install --no-cache-dir -r {}".format(requirements_file))
        else:
            raise FileNotFoundError(requirements_file)

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

    def __set_container(self, container):
        self.__container = container

        with open(os.path.join(self.__path, "container"), "wb") as container_file:
            container_file.write(pickle.dumps(container))

    def __get_container(self):
        container = None

        if os.path.exists(os.path.join(self.__path, "container")):
            with open(os.path.join(self.__path, "container"), "rb") as container_file:
                container = pickle.load(container_file)

        return container
