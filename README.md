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

### Working with requirements
The current version of Cage only supports dependencies **written in a requirements file**:
```bash
(<name_of_your_cage>)$ pip install -r requirements.txt
```

You *cannot* use any other pip commands with this version. This includes simple pip install commands like:
```bash
(<name_of_your_cage>)$ pip install <dependency>
```

### Deactivating the environment
```bash
(<name_of_your_cage)$ deactivate
```

This will return your environment to the state it was in before activating the Cage environment.

## Caveats
1. **THIS IS A WORK IN PROGRESS. DO NOT USE THIS IF YOU DON'T KNOW WHAT YOU ARE DOING** 
2. You can **only** use pip with a requirements file. No other pip commands are supported.
3. No ports are exposed from the docker container at the moment
4. Environment variables are not sent to the docker container

## License
Cage is released under the MIT license. See LICENSE for details.

## Contact
Follow me on twitter [@mcostea](https://twitter.com/mcostea)
