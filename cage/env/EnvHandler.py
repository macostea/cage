import os
import stat
import shutil


class EnvHandler:
    def __init__(self, binaries_path):
        self.__binaries_path = binaries_path

    def init_env(self, env_path):
        new_bin_path = os.path.join(env_path, "bin")

        if not os.path.exists(new_bin_path):
            os.makedirs(new_bin_path)

        self.__update_activate_script(os.path.join(self.__binaries_path, "activate.sh"), new_bin_path)

        self.__copy_other_binaries(self.__binaries_path, new_bin_path)

    def __update_activate_script(self, activate_script_path, destination_script_path):
        new_activate_script_path = os.path.join(destination_script_path, "activate")

        # Copy the file
        shutil.copyfile(activate_script_path, new_activate_script_path)

        # Update the activate data
        activate_data = None
        with open(new_activate_script_path, "r") as file:
            activate_data = file.read()

        activate_data = activate_data.replace("__CAGE_ENV__", destination_script_path)

        with open(new_activate_script_path, "w") as file:
            file.write(activate_data)

    def __copy_other_binaries(self, binaries_path, destinaton_binaries_path):
        shutil.copyfile(os.path.join(binaries_path, "python.sh"), os.path.join(destinaton_binaries_path, "python"))
        old_stat = os.stat(os.path.join(destinaton_binaries_path, "python"))
        os.chmod(os.path.join(destinaton_binaries_path, "python"), old_stat.st_mode | stat.S_IEXEC)

        shutil.copyfile(os.path.join(binaries_path, "pip.sh"), os.path.join(destinaton_binaries_path, "pip"))
        old_stat = os.stat(os.path.join(destinaton_binaries_path, "pip"))
        os.chmod(os.path.join(destinaton_binaries_path, "pip"), old_stat.st_mode | stat.S_IEXEC)
