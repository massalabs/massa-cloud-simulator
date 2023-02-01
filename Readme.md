# Massa cloud simulator
### Pre-requisites
- Make sur you have [Docker](https://www.docker.com/) installed and running on your computer, however you can find informations about how to install Docker [here](https://docs.docker.com/get-docker/).

- You also need to have [Python3](https://www.python.org/download/releases/3.0/) installed on your device in order to launch the simulator, you can download it [here](https://www.python.org/downloads/).

---
## Environment variables

You have to **_edit_** the `env.sample` file by **_replacing_** the content in order to use your own configuration.

After that, let's **_copy_** the `env.sample` file to a new file `.env` using the folowing command:
```sh
    cp -v env.sample .env
```

---
## Launch the Cloud Simulator

We can launch the **_simulator_** with the line bellow :
```sh
    ./launch.sh
```

---
## Testing part

- ### **Create a virtual environment with good dependencies**

```sh
    python3 -m venv venv
    venv/bin/pip install -r requirements_tests.txt
```

- ### **Launch our test script**
```sh
    venv/bin/python test_1.py
```

---
## Optional part (Good to know)

### Acces to the container **environment** while running
```sh
    docker exec -it [container_name] bash
```

### To see the **logs** of a container :
```sh
    docker logs -f [container_name]
```

### To get the **IP Address** of severals containers :
```sh
    docker container inspect [container_name_1] [container_name_2] | grep -i IPAddress
```
