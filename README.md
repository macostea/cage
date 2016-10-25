# Cage
Develop and run your Python applications in clean Docker environments
Cage aims to be as easy to use and as familiar as possible.

## Requirements
* Docker
* Python 3.5+

## Installation
```bash
$ pip install pycage 
```

## Usage
NOTE: Docker should be running before using any of the Cage commands.
All commands should be run from your project directory!

### Create a new cage
```bash
$ cage app:create <name_of_your_cage>
```

This command will create a new Dockerfile in the root your project and initialize all the necessary environment files.

### Activate the new environment
```bash
$ source <name_of_your_cage>/bin/activate
```

This command should be very familiar to [virtualenv](https://virtualenv.pypa.io/en/stable/) users. This adjusts your environment to make sure you use the caged python binaries.

### Run your project
```bash
(<name_of_your_cage>)$ python <file.py>
```

Running a script with the caged python binary will build a new Docker image with your project files, create a new container using that image and run the python command you specified.

### Passing environment variables
You can pass environment variables to the cage by creating a **ENV** file in the root of your project. The file structure should be VAR=VALUE.

Example:
```
AVAR=value1
BVAR=value2
```

You can also place this file anywhere in your project. If it is not in the root of your project you can specify the path to it by passing the ENV variable when running a python script.

```bash
(<name_of_your_cage>)$ ENV=path/to/ENV python <file.py>
```

### Expose a TCP Port
To expose a TCP port from the cage, use the PORT environment variable defined in your ENV file.

Example:
```
PORT=5000
```

Specifying it in the ENV file will also make it available in the cage so you can bind your apps to it easily.

### Working with requirements
The current version of Cage only supports dependencies **written in a requirements file**:
```bash
(<name_of_your_cage>)$ pip install -r requirements.txt
```

You *cannot* use any other pip commands with this version. This includes simple pip install commands like:
```bash
(<name_of_your_cage>)$ pip install <dependency>
```

### Stop a cage
```bash
(<name_of_your_cage>)$ cage app:stop <name_of_your_cage>
```

### Deactivating the environment
```bash
(<name_of_your_cage)$ deactivate
```

This will return your environment to the state it was in before activating the Cage environment.

## Caveats
1. **THIS IS A WORK IN PROGRESS. DO NOT USE THIS IF YOU DON'T KNOW WHAT YOU ARE DOING** 
2. You can **only** use pip with a requirements file. No other pip commands are supported
3. You can only expose **ONE TCP** port from the container and it will be mapped to the same port number on the host
4. Tested only on OSX and Linux

## License
Cage is released under the MIT license. See LICENSE for details.

## Contact
Follow me on twitter [@mcostea](https://twitter.com/mcostea)
