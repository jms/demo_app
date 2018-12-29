# demo_app

Run:
```bash
pipenv run flask run
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
