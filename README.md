
# Notes API

Welcome to the Notes API with Full Text Search using Elasticsearch! This project provides a robust API for managing and searching notes seamlessly. Users can create, update, delete, and retrieve notes while leveraging the power of Elasticsearch for lightning-fast full-text search capabilities. The API is built on Flask, SQLAlchemy, and Elasticsearch, ensuring a reliable and scalable solution for handling your note-taking needs.
## Features

- User authentication using [JWT](https://jwt.io/introduction) .
- Authenticated users can create, update, delete and retrieve their notes.
- Full text search over notes title and content using [Elasticsearch](https://en.wikipedia.org/wiki/Elasticsearch) providing lightning-fast full-text search capabilities.
- Payload validations for both requests and responses are present and done using [Marshmallow](https://marshmallow.readthedocs.io/en/stable/).
- API responses in case of errors and normal responses follow a structure, making it easier for the frontend to parse and make sense of the JSON response.


## Run Locally

Clone the project

```bash
  git clone https://link-to-project
```

Go to the project directory

```bash
  cd my-project
```

### Using Docker

We can use Docker to run the project. It would make sure all dependencies are installed.

To install Docker, follow steps below according to your operating system:

- [Linux](https://docs.docker.com/desktop/install/linux-install/)
- [Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Mac](https://docs.docker.com/desktop/install/mac-install/)

After Docker is installed, run the project:

```bash
docker-compose down --volumes --remove-orphans && docker-compose up --build api
```
This would start the API which will be available at port `8080`.

### Without Docker

If you don't wan't to use Docker, you will have to have following items installed on your device:

- Python (3.8+ preferred)
- Elasticsearch(8.7.1 preferred)
- Postgresql (13.4 preferred, modify environment variables to use other RDBMS supported by [SQLAlchemy](https://www.sqlalchemy.org/features.html#:~:text=Supported%20Databases,of%20which%20support%20multiple%20DBAPIs.))

If you have all these installed, you are good to go.

To install dependencies (usage of [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) preferred)

```bash
pip install -r requirements.txt
```

Ensure that Elasticsearch is up and running at a port specified by environment variable (default is `9200`)

To start the API

```bash
python app.py
```

This would start the API on port `8080` by default.
## Running Tests

To run tests, run the following command(s)

### Using Docker

```bash
  docker-compose down --volumes --remove-orphans && docker-compose up --build test
```

### Without using Docker

First install extra dependencies

```bash
pip install -r requirements-text.txt
```

Use [Pytest](https://docs.pytest.org/en/7.4.x/) to run tests

```bash
pytest -vvv
```
## Environment Variables

To run this project, you will need to add some environment variables to your .env file

If environment variables are not defined, API will use default values which you can figure out by checking code.

Example environment file is present by the name `.env.example`

Some common environment variables used in this API are

```env
HOST=localhost
PORT=8080
DEBUG=True
ELASTICSEARCH_PASSWORD=hecker
ELASTICSEARCH_USER=elastic
POSTGRES_PASSWORD=root
POSTGRES_USER=root
POSTGRES_DB=notesapp
DATABASE_URL=postgresql://root:root@localhost:5432/notesapp
ELASTICSEARCH_URL=https://localhost:9200
SECRET_KEY=secret
```

## API Reference

### Authentication

#### Get JWT auth and refresh tokens

_Request_

```http
POST /api/auth/login HTTP/1.1
Host: localhost:8080
Content-Type: application/json
Content-Length: 53

{
    "username": "root",
    "password": "root"
}
```

_Response_

```json
{
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDYzMjQ4MCwianRpIjoiZTQ5NTdkODAtYjY3NC00NGQ0LTk1NWItNWQ4ZjdmM2Q3ZmU1IiwidHlwZSI6InJlZnJlc2giLCJzdWIiOjExLCJuYmYiOjE3MDQ2MzI0ODAsImNzcmYiOiIzYTZmZDA5Ny0yNzA3LTRmMDQtOWJmNC1kY2QzMjQ1ZjkwZTMiLCJleHAiOjE3MDcyMjQ0ODB9.pJrcMXEtzz66Pn2v9vwamRPeMjQUH_gA5bWH_hcL0lg",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcwNDYzMjQ4MCwianRpIjoiMDc0OGVmODktYWY1Ny00NmI2LWIxMjMtZGJhZmMxOWI5NDRkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MTEsIm5iZiI6MTcwNDYzMjQ4MCwiY3NyZiI6ImQzNmZjNzIyLThiZjItNGQ1Zi04ZTk3LTUzZGRkNTc5MWMwMiIsImV4cCI6MTcwNDYzMzM4MH0.mAPCCGNRP3C2GMKJcrhkBbjSmnAVxhq4FTGU8EqwbEA"
}
```

Returns refresh and auth tokens in case of successful login.

#### Register new user

_Request_

```http
POST /api/auth/register HTTP/1.1
Host: localhost:8080
Content-Type: application/json
Content-Length: 60

{
    "username": "randomUser",
    "password": "root" 
}
```

_Response_

```json
{
    "data": {
        "username": "randomUser",
        "created_at": "2024-01-07T13:02:10.877313",
        "updated_at": "2024-01-07T13:02:10.877313",
        "id": 13
    },
    "status_code": 201
}
```

Registers a new user to the platform.

### Notes

#### Get all notes

_Request_

NOTE: Login Required

```http
GET /api/notes HTTP/1.1
Host: localhost:8080
Authorization: Bearer <auth token here>
```

_Response_

```json
{
    "data": [
        {
            "title": "hecker",
            "content": "A good note",
            "created_at": "2024-01-03T19:19:52.528078",
            "updated_at": "2024-01-03T19:19:52.528078",
            "user_id": 11
        },
        {
            "title": "i am hecker",
            "content": "A good note",
            "created_at": "2024-01-03T21:33:23.746951",
            "updated_at": "2024-01-03T21:33:23.746951",
            "user_id": 11
        }
    ],
    "count": 2,
    "status_code": 200
}
```

#### Get note by id

_Request_

NOTE: Login Required

```http
GET /api/notes/<id: number> HTTP/1.1
Host: localhost:8080
Authorization: Bearer <auth token here>
```

_Response_

```json
{
    "data": {
        "id": 1,
        "title": "f",
        "content": null,
        "created_at": "2024-01-03T19:16:16.246375",
        "updated_at": "2024-01-05T05:30:43.905018",
        "user_id": 11
    },
    "status_code": 200
}
```

#### Create Note

NOTE: Login Required

```http
POST /api/notes HTTP/1.1
Host: localhost:8080
Authorization: Bearer <auth token here>
Content-Type: application/json
Content-Length: 50

{
    "title": "test ",
    "content": "test"
}
```

_Response_

```json
{
    "data": {
        "title": "test ",
        "content": "test",
        "created_at": "2024-01-07T10:10:07.984095",
        "updated_at": "2024-01-07T10:10:07.984095",
        "user_id": 11,
        "id": 1
    },
    "status_code": 201
}
```

#### Update Note by ID

NOTE: Login Required

```http
POST /api/notes/<id: number> HTTP/1.1
Host: localhost:8080
Authorization: Bearer <auth token here>
Content-Type: application/json
Content-Length: 29

{
    "title": "not test"
}
```

_Response_

```json
{
    "data": {
        "title": "not test ",
        "content": "test",
        "created_at": "2024-01-07T10:10:07.984095",
        "updated_at": "2024-01-07T10:10:07.984095",
        "user_id": 11,
        "id": 1
    },
    "status_code": 200
}
```

#### Delete Note by ID

_Request_

NOTE: Login Required

```http
DELETE /api/notes/<id: number> HTTP/1.1
Host: localhost:8080
Authorization: Bearer <auth token here>
```

_Response_

```json
{
    "data": {
        "id": 1,
        "title": "i am hecker",
        "content": "A good note",
        "created_at": "2024-01-03T21:35:51.221179",
        "updated_at": "2024-01-03T21:35:51.221179",
        "user_id": 11
    },
    "status_code": 200
}
```

#### Full text search in notes

_Request_

NOTE: Login Required

```http
GET /api/notes/search?q=<query string> HTTP/1.1
Host: localhost:8080
Authorization: Bearer <auth token here>
```

_Response_

```json
{
    "data": [
        {
            "id": 11,
            "title": "what is hecker",
            "content": "who am i",
            "created_at": "2024-01-03T21:39:41.007369",
            "updated_at": "2024-01-03T21:39:41.007369",
            "user_id": 11
        },
        {
            "id": 20,
            "title": "what ",
            "content": "who is hecker",
            "created_at": "2024-01-04T23:48:09.514412",
            "updated_at": "2024-01-04T23:48:09.514412",
            "user_id": 11
        }
    ],
    "count": 2,
    "status_code": 200
}
```
## Tech Stack

**Server:** Python as Programming Language, Flask as Web Framework, SQLAlchemy as ORM

**Databases:** Postgresql and SQLite to store data for production and tests respectively, Elasticsearch for fast inverted index search

**Authentication:** JWT is used for Authentication


## TODO

- [ ]  Add documentation for API
- [ ]  Make notes sharing feature
- [ ]  Add Pagination to API
- [ ]  Handle flask-jwt-extended errors
- [ ]  Fix bugs if found 

## License

[MIT](https://choosealicense.com/licenses/mit/)

