# User-CRUD-App

User-CRUD App

## Endpoints

[View on Heroku](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/)

| EndPoint                                             | Functionality                                    |
| ---------------------------------------------------- | ------------------------------------------------ |
| [POST   /api/v1/users](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/#!/User/post_api_v1_users)                       | Register a user                              |
| [PUT    /api/v1/users/\<userId>](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/#!/User/put_api_v1_users_user_id)         | Updates a user                       |
| [DELETE /api/v1/users/\<userId>](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/#!/User/delete_api_v1_users_user_id)         | Remove a user                                |
| [GET    /api/v1/users](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/#!/User/get_api_v1_users)                       | Retrieves all users                         |
| [GET    /api/v1/users/\<userId>](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/#!/User/get_api_v1_users_user_id)         | Get a user                                   |

## Tested with

* Python 3.6
* PostgreSQL 11

## Requirements

* Install [Python](https://www.python.org/downloads/)
* Install [PostgreSQL](https://www.postgresql.org/download/)

## Setup (MAC/Linux)

* Run `git clone` this repository and `cd` into the project root.
* Run `pip install virtualenv`.
* Run `virtualenv ../user-crud-venv --python=python3`.
* Run `source ../user-crud-venv/bin/activate`.
* Run `pip install -r requirements.txt`.
* Run `createdb <user_crud_db>` on the psql bash terminal
* Run `export DATABASE_URL=postgresql://<db_user>:<password>@localhost/<user_crud_db>`
* Run `export SECRET_KEY=<some_secret_value>`
* Run `export FLASK_CONFIG=development`.

## Setup (Windows)

* Run `git clone` this repository and `cd` into the project root.
* Run `pip install virtualenv`.
* Run `pip install virtualenvwrapper-win`.
* Run `set WORKON_HOME=%USERPROFILES%\Envs`.
* Run `mkvirtualenv venv`.
* Run `workon venv`.
* Run `pip install -r requirements.txt`.
* Run `createdb <user_crud_db>` on the psql bash terminal
* Run `set DATABASE_URL=postgresql://<db_user>:<password>@localhost/<user_crud_db>`
* Run `set SECRET_KEY=<some_secret_value>`
* Run `set FLASK_CONFIG=development`.

## Setup --continued

* Run the following.
  * `python3 manage.py db init` to create a migration repository
  * `python3 manage.py db migrate` to update the migration script
  * `python3 manage.py db upgrade` to apply the migration to the database
* Run `python3 manage.py runserver`. to run on the default ip and port
* View the app on `http://127.0.0.1:5000/`

## Use endpoints

* View the api on `http://127.0.0.1:5000/api/v1/`
* Test it's usage with postman

## Use api documentation

* View the api on [Heroku](https://user-crud-api-v1-rwothoromo.herokuapp.com/apidocs/)
* View the api on `http://127.0.0.1:5000/apidocs`

## Notes

For detailed instructions on heroku deployments, go [here](https://medium.com/@johnkagga/deploying-a-python-flask-app-to-heroku-41250bda27d0) or [here](https://devcenter.heroku.com/articles/heroku-cli)
