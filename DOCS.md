## Getting Started
there is a swagger document on     
```
http://localhost:8000
```

## complex queries

### login
POST /api/auth/jwt/login/
```
{
  "username": "bita",
  "password": "8125687g@"
}
```
and then copy access token and past it on Authorize
botton on the top of the swagger ui
or on curl
```
curl -X 'GET' \
  'http://localhost:8000/api/blog/post/?search=foo' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer access_token'
```

### get posts
Get /api/blog/post/

created_at
```
?created_at__range=2022-10-27,2022-10-27
```

authors
```
?author__in=admin,amirbahador
```

full_text_search
```
?search=foo
```

