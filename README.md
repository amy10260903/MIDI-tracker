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
