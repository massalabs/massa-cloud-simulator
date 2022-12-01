# Massa cloud simulator
### Pre-requisites
- Make sur you have [Docker]("https://www.docker.com/") installed and running on your computer, however you can find informations about how to install Docker [here]("https://docs.docker.com/get-docker/").
---
### Environment variables
You have to **_create_** your own .env file.
Then you can put the following content in your .env file :
```sh
    user="user"
    user_pswd="user"
```
---
### Launch the docker-compose
On a **_first terminal window_**, let's launch our **_P.O.C_** with the line bellow :
```sh
    docker-compose up --build
```
---
### Acces to the container environment
* On a **_second terminal window_**, launch the following command :
```sh
    docker exec -it poc-testnet-1 bash
```
> "poc-testnet-1" correspond to your first container
---
* On a **_third terminal window_**, let's run your second container :
```sh
    docker exec -it poc-testnet-2 bash
```
> "poc-testnet-2" correspond to your second container
---
