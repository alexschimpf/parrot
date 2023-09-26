## Parrot 🦜

### Summary
<hr>

Parrot is a simple mock server, mainly intended for dev/CI use.
You can configure Parrot to return mock responses based on given request data.
For example, you could configure it to behave like so:

```
GET /something?q=1
=>
{
    "some": "mock data"
}

GET /something?q=2
=>
{
    "some": "other mock data"
}
```

You can specify custom mocking rules to return the responses you want.
- Match HTTP method
- Match URL path
- Match query parameters
- Match headers
- Match cookies

You can also specify some of these parameters as optional, meaning they will be matched only if they are present in the request data,
In many cases, static responses may not be enough. You may want more dynamic control over responses.
In these cases, you can provide Python code, which generates response data (e.g. body, headers, status) on the fly.
Your Python code can access all necessary request data (e.g. HTTP method, URL path, request data, query parameters, headers, and cookies).

Parrot has a simple REST API for managing mock rules via CRUD operations.
You can also load your rules into Parrot's docker container using bind mounts.

### Installation
<hr>

Install the docker image:
```shell
$ docker image pull alexschimpf/parrot
```

Run the docker container:
```shell
$ docker run -p 5000:80 alexschimpf/parrot
```
This will run a FastAPI/Uvicorn server, listening on port 5000.
You can view the API docs at: http://127.0.0.1:5000/docs.

If you want to load your own mock rules into the container, you can do so via bind mounts:
```shell
$ docker run -p 5000:80 -v <rules-dir>:/parrot/rules -v <handlers-dir>:/parrot/handlers alexschimpf/parrot
```
This will bind directories on your local file system to directories in the Parrot container.

### Mock Rules
<hr>

#### Specs
<hr>

Mock rules can be managed by via the API's CRUD endpoints.
The Swagger docs describe the inputs/outputs.

If you want to load mock rules into your docker container, you'll need to understand the required format.
Mock rules are specified via JSON files. Handlers are specified via Python files as described below in the *Dynamic Response Handlers* section.

Here is an example mock rule JSON file:
```json
{
    "<rule1>": {
        "name": "<rule1>",
        "method": "PUT",
        "path": "/blah/123",
        "query_params": {
            "q": "1",
            "?opt": "whatever"
        },
        "headers": {
            "Content-Type": "application/json",
            "?Auth-Key": "blah"
        },
        "cookies": {
            "test": "1",
            "?blah": "321"
        },
        "response_body": {
            "some": "thing"
        },
        "response_status": 200,
        "response_headers": {
            "header1": "abc"
        }
    },
    "<rule2>": {
        "name": "<rule2>",
        "method": "GET",
        "path": "/blah/345",
        "query_params": {
            "q": "1",
            "?opt": "whatever"
        },
        "headers": {
            "Content-Type": "application/json",
            "?Auth-Key": "blah"
        },
        "cookies": {
            "test": "1",
            "?blah": "321"
        },
        "response_handler": "response = { 'body': 'test!', 'status': 201, 'headers': { 'header1': 'abc' }  }"
    }
}
```
- The rule with name/key `rule1` describes a rule where a static response is returned when the request context is matched.
  - A request is matched using the following logic:
    - Request method must be "PUT"
    - The request path must be "/blah/123"
    - A query param "q" must be present with value "1", and if, and only if, a query param "opt" is present, it must have value "whatever".
      - Note that if a key starts with "?", it is considered optional.
    - A header "Content-Type" must be present with value "application/json", and if, and only if, a header "Auth-Key" is present, it must have value "blah".
    - A cookie "test" must be present with value "1", and if, and only if, a cookie "blah" is present, it must have value "321".
  - If the request is matched, it will return a JSON body `{"some": "thing"}`, with status code 200, and a single header `header1: abc`.
    - Note that you may need to include a `Content-Type` header. JSON will automatically be detected though, and a `Content-Type: application/json` header will automatically be added.
- The rule with name/key `rule2` describes a rule where a dynamic response is returned when the request context is matched.
  - The matching logic is similar to what was described above
  - The response, however, is generated via the `response_handler` value. Response handler values can take one of two forms:
    - It can be an inline string that contains Python code (compatible with Python 3.11).
    - It can be a string representing an external Python file
      - The value must begin with "file::" with the file path following that. The file path should be relative to `/parrot/handlers`.
      - This file must exist in the `/parrot/handlers` directory by binding a local directory to a directory in the container.
        - External Python files can only be loaded this way. They cannot be added to Parrot via the API.
      - More details can be found below in the *Dynamic Response Handlers* section.

#### API
<hr>

The API swagger docs can be found at: http://127.0.0.1:5000/docs (or whatever port you chose).
There are various CRUD endpoints for adding, removing, and viewing mock rules.
Mock rules are written to a JSON file on disk in the container.

#### Bind Mounts
<hr>

As described above in the *Installation* section, mock rules can be loaded into the container on startup via Docker bind mounts.
There are 2 directories which can be mounted to:
- /parrot/handlers
    - This is for Python files used for dynamic response handling
    - This is described in more details below in the *Dynamic Response Handlers* section
    - These files are to be referenced by mock rules
    - These files should typically have the `.py` extension
- /parrot/rules
    - This is for JSON mock rule files as described in the *Specs* section
    - These files should typically have the `.json` extension

The files are automatically loaded into memory when the server starts up.

### Dynamic Response Handlers
<hr>

Dynamic responses can be generated at runtime using custom Python files.
These files can be written inline into mock rules or can be separate files referenced by mock rules.
Python code should be compatible with Python 3.11.

Response handlers can access request context via the following variables:
- method
  - Type: String
  - HTTP method
- path
  - Type: String
  - Always starts with a forward slash
  - This is the part of the URL path that comes after "/match"
- query_params
  - Type: `starlette.requests.QueryParams`
  - This can be used like a dict
  - Contains query param string key/values
- headers
  - Type: `starlette.requests.Headers`
  - This can be used like a dict
  - Contains header string key/values
- cookies
  - Type: dict[str, str]
  - Contains cookie key/values
- body
  - Type: string
  - Request body

Response data should NOT be returned from your code.
Instead, a `response` variable should be assigned like so:
```Python
response = {
    'body': 'blah',
    'status': 200,
    'headers': {
        'some': 'header'
    }
}
```
Notes:
- The `body` field is the only one required. The other two are optional and don't need to be set/defined.
- The `json` module is imported automatically. This can be used to load JSON objects from strings or dump JSON objects to strings.
