# Travel planning app

## Goals

This app is dedicated to the optimisation of traveling plans. 

## Features


## Quickstart

First, rename the .env.example file in .env.

Then change the values corresponding to the one you will be using.

### Using docker

```
docker-compose up -d --build
```

### Locally

1. Start the database
    1) Set up your .env file, copy .env.example in .env and change the value corresponding to your environnement.
    2) Then execute the following :
```
docker compose up -d db
```

2. Start the backend
    1) Head to ()[back/README.md]
```
cd back && python app.py
```

3. Start the frontend
```
cd ../front && npm run dev
```
