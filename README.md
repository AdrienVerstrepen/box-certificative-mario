# Travel planning app

## Goals

This app is dedicated to the optimisation of traveling plans. 

## Requirements

- Python3+
- Node 22+
- PostgresSQL Server (if not using docker)

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
    2) Then load the demo-db.sql into your PostgreSQL server database.

2. Start the backend
    1) Set up your environnements variables
- On Windows cmd : 
```
set POSTGRES_USER_PASSWORD=SAME_AS_IN_.ENV
set POSTGRES_DATABASE=SAME_AS_IN_.ENV
set POSTGRES_USER=SAME_AS_IN_.ENV
set DB_HOST=SAME_AS_IN_.ENV
set DB_PORT=SAME_AS_IN_.ENV
```
- On Linux :
```
export POSTGRES_USER_PASSWORD=SAME_AS_IN_.ENV
export POSTGRES_DATABASE=SAME_AS_IN_.ENV
export POSTGRES_USER=SAME_AS_IN_.ENV
export DB_HOST=SAME_AS_IN_.ENV
export DB_PORT=SAME_AS_IN_.ENV
```
    2) Install the requirements in the "back" directory : 
```
pip install -r requirements
```
    3) Start the back-end : 
```
cd back && python app.py
```

3. Start the frontend
    1) Go to the "front" directory 
    2) Install the dependencies using ``npm i``
    3) Start the dev server using ``npm run dev``