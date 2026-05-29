# Travel planning front-end

## Presentation

This directory holds the source code of the back end off this travel planning app.

## Quickstart

Once you have set up the correct variables in the .env file, please enter the following commands if not launching the app through docker :

- On Windows cmd : 
```
set POSTGRES_USER_PASSWORD=password2
set POSTGRES_DATABASE=database_name
set POSTGRES_USER=database_user_name
set DB_HOST=localhost
set DB_PORT=5432
```
- On Linux :
```
export POSTGRES_USER_PASSWORD=password2
export POSTGRES_DATABASE=database_name
export POSTGRES_USER=database_user_name
export DB_HOST=localhost
export DB_PORT=5432
```

Once done, please start the app using : 

```
python app.py
```

## Tests launch
The tests for the algorithm side can be launched with the following commands :

```
python -m unittest back.algorithm.tests.cluster_manager_test
python -m unittest back.algorithm.tests.dynamic_held_karp_test
python -m unittest back.algorithm.tests.location_test
python -m unittest back.algorithm.tests.nearest_neighbours_test
python -m unittest back.algorithm.tests.tour_test
```