# MIDI Tracker
Generate midi chord tracks with a midi chord.

## Quick Start
### Install with Docker
#### Setup
Install Docker and Docker compose
```shell
$ chmod +x deploy/setup.sh
$ ./setup.sh
```
#### Build and run with Docker compose
Start the server at http://127.0.0.1:8000
```shell
$ docker compose up --build
``` 

### Install with pip
#### Installation
```shell
$ pip install -r deploy/requirements.txt
```

#### Run the server
Start the server at http://127.0.0.1:8000
```shell
$ cd midi_tracker
$ python manage.py runserver
```

## Credit
Credits to the creators on [Flaticon](https://www.flaticon.com).
The followings are the icons used in this project,
- <a href="https://www.flaticon.com/free-icons/synthesizer" title="synthesizer icons">Synthesizer icons created by Pixel Buddha Premium - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/cloud-computing" title="cloud computing icons">Cloud computing icons created by Smartline - Flaticon</a>
- <a href="https://www.flaticon.com/free-icons/electric-keyboard" title="electric keyboard icons">Electric keyboard icons created by Pixel perfect - Flaticon</a>
