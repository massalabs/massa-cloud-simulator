# Massa cloud simulator
### Pre-requisites
- Make sur you have [Docker]("https://www.docker.com/") installed and running on your computer, however you can find informations about how to install Docker [here]("https://docs.docker.com/get-docker/").
---
### Environment variables

You have to **_edit_** the `env.sample` file by **_replacing_** the content in order to use your own configuration.

After that, let's **_copy_** the `env.sample` file to a new file `.env` using the folowing command:
```sh
    cp -v env.sample .env
```
---
### Launch the docker-compose
We can launch our **_P.O.C_** with the line bellow :
```sh
    docker-compose up --build
```

---

## Optional part
### Acces to the container **environment**
```sh
    docker exec -it [container_name] bash
```
---
### To see the **logs** of a container :
```sh
    docker logs -f [container_name]
```
---
### To get the **IP Address** of severals containers :
```sh
    docker container inspect [container_name_1] [container_name_2] | grep -i IPAddress
```
