# demo_app

Setup:

- Create a empty postgresql database

- Create the dot env file

```bash
touch .flaskenv  # or touch .env
```

add to the `.flaskenv` file the required variables:

```ini
FLASK_ENV=development
FLASK_DEBUG=1
SQLALCHEMY_DATABASE_URI=postgresql://username:password@host:5432/database
SECRET_KEY=<secret key>
SALT=<salt key>
```

Run:

```bash
poetry install  # install packages
poetry run flask run  # run the app

```

test:

```bash
bash$ time -p curl -H "Content-Type: application/json" \
-X POST -d '{"email":"test@example.com","password":"test"}' \
http://127.0.0.1:5000/login
```

```json
{
  "meta": {
    "code": 200
  },
  "response": {
    "user": {
      "authentication_token": "<token>",
      "id": "1"
    }
  }
}
```

```bash
bash$ time -p curl -H 'Authentication-Token:<token>' http://localhost:5000/hello
```

```text
{
  "hello": "world"
}
real 0.02
user 0.00
sys 0.00

```
