## Massa cloud simulator

# Pre-requisites
- Make sur you have docker installed and running on your computer

---
# Environment variables
You have to **create** your own .env file.
For example, you can put the following content in your .env file :
```sh
    user="user"
    user_pswd="user"
```

---
# Launch the docker-compose
Lets launch our **P.O.C** with the line bellow :
```sh
    docker-compose up --build
```

---
# Acces to the container environment
```sh
    docker exec -it poc-testnet-1 bash
```
> poc-testnet-1 correspond to your container
---