# demo_app

test: 

```bash
time -p curl -H "Content-Type: application/json" -X POST -d '{"email":"test@example.com","password":"test"}' http://127.0.0.1:5000/login
```

```json
{
  "meta": {
    "code": 200
  }, 
  "response": {
    "user": {
      "authentication_token": "WyIxIiwiJDEkZFlFNXpiQXMkRWJUUFNsUWRyY2JJaGVpd1htNy41MSJd.DrTiPw.MOe_885QQTbkg1kPaEUJsZ9BinY", 
      "id": "1"
    }
  }
}
```

```bash
time -p curl -H 'Authentication-Token:WyIxIiwiJDEkZFlFNXpiQXMkRWJUUFNsUWRyY2JJaGVpd1htNy41MSJd.DrTiPw.MOe_885QQTbkg1kPaEUJsZ9BinY' http://localhost:5000/hello
```

```text
{
  "hello": "world"
}
real 0.02
user 0.00
sys 0.00

```
