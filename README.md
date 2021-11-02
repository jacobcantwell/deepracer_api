# Deepracer_api Rewirte
This project base on https://github.com/thu2004/deepracer-vehicle-api rewrite to support the new version Deepracer Console `Software version 1.0.606.0`

## Pygame

Pygame is a set of Python modules designed for writing video games. https://www.pygame.org/news.html

This project uses pygame joystick library as input data for the DeepRacer APIs.

# Directory Tree
```
deepracer_api/
├── config.yml
├── core
│   ├── deepracer_cam.py
│   ├── __init__.py
│   └── logger.py
├── docker
│   ├── cam
│   │   └── Dockerfile
│   ├── g29
│   │   └── Dockerfile
│   └── ps4
│       └── Dockerfile
├── docker-compose.g29.yml
├── docker-compose.ps4.yml
├── g29_mode.py
├── logs
├── ps4Controller_mode.py
├── README.md
├── requirements.txt
├── setup.sh
├── show_cam.py
├── start-g29.sh
├── start-ps4.sh
└── test
    ├── os_test.py
    ├── ps4Controller_test.py
    └── test_g29.py

```
# Local Setup

If You don't need to build the docker then need config the virtual environment for run this projcet.

```bash
$Powershell
> git clone https://github.com/jacobcantwell/deepracer_api.git
> cd deepracer_api
> python -m venv venv
> .\venv\Scripts\activate
> pip install -r requirements.txt
```

```bash
$linux
> git clone https://github.com/jacobcantwell/deepracer_api.git
> cd deepracer_api
> python3 -m venv venv
> . venv/bin/activate
> pip install -r requirements.txt
```

To test that the joysticks work with the Pygame library

```bash
python .\test\pygame_joystick_simple_test.py
python .\test\pygame_joystick_full_test.py
```

To control with a PS4 joystick

```bash
python ps4_mode.py
```

To show the camera feed

```bash
python show_cam.py
```

### When you finish you just need to config the `config.yml` to fill your deepracer ip and password.

- replace the code
```py 
client = Client(password=os.getenv("password"), ip=os.getenv("hostIp"))
```

```py
    dir_path = os.path.dirname(os.path.realpath(__file__))

    with open(os.path.join(dir_path, "config.yaml"), "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    
    client = Client(cfg["password"], cfg["ip"])
```

# Docker setup
- run the `setup.sh` file to setup your IP and password it will generate a `hostname_passord` file to save your IP and password.

- choose which mode you need then run to `start` sh file


docker run -it --rm --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" g29

docker run -it --rm -e password=xxxx -e hostIp=yyyy g29

* Set environmental variables with Python Decouple https://pypi.org/project/python-decouple/
    * Create a .env file in your root directory
    * Add values for
      * LOCAL_IP=[local-ip] - the local IP address of the car in format ###.###.###.###
      * DEEPRACER_PASSWORD=[password] - string with the password value used to login to the DeepRacer UI



# Other
- Testing on Windows, Ubuntu, MacOS (with USB port)
- G29 Mode is not supporting on Linux