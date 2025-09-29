# Serverless REST API Backend Development Instructions

## Overview

You are developing a serverless REST API backend for a frontend application.
Each function operates independently, is scalable, and stateless without shared code.

You have to always write unit and integration tests for each action.
Unit tests must invoke directly the action function passing dictionaries.

Integration test must use the requests library and perform HTTP requests to the deployed action endpoints, 
using as host the `OPSDEV_HOST` environment variable.

You can execute an unit test in isolation, as they use test containers.
When you change the code of an action, before executing the integration test,
you have to redeploy it with `ops ide deploy <package>/<action>`.

## Goals

- Code Python REST API backend functions
- Support an existing JavaScript frontend (generated with Lovable) that **MUST NOT** be modified
- Each deployed action becomes a REST endpoint at `/api/my/<package>/<name>`

## Project Structure

### Action Organization

- Actions are stored in `packages/<package>/<name>/*.py`
- Each action requires a `packages/<package>/<name>/__main__.py` file
- Each action has an `<action>.py` file with a `main` function
- Unit tests: `tests/<package>/test_<name>.py`
- Integration tests: `tests/<package>/test_<name>_int.py`

### Function Structure

- Main function receives JSON object input and returns JSON object output (never arrays or primitives)
- `__main__.py` ends with: `return {"body": <action>.<action>(args) }`
- Write code in `<action>.py` file within the `<action>` module, **never** in `__main__.py`
- Always add annotation comments (format: `#--`) in `__main__.py`

### Common Annotation

Each action must specify its kind, so it needs always

```
#--kind python:default
```

Action that are invoked publicly also need to be exposed with

```
#--param true
```

## Development Commands

### Creating Actions

```bash
ops lv new <action> <package>
```

### Deployment

Before any deployment you need credentials, stored in `~/.wskprops`.
If there is not a `~/.wskprops` file you need to create it logging into the system:

```bash
ops ide login
```

# Deploy single action

```bash
ops ide deploy <package>/<action>
```

If you need to add parameters to the action, add them in `__main__.py`
as a comment `#--param <PARAM_NAME>  <PARAM_VALUE>`

A <PARAM_VALUE> is a shell expression and can use variables, in the format `"$VARIABLE`.

Variables can be defined in `.env` or be one of the service secrets provided by the system.

# Deploy all actions

```bash
ops ide deploy
```

## Environment and Dependencies

### Limitations

- Write **only Python code**, not JavaScript
- Consider only `packages/*` and `tests/*` folders
- **NEVER** use `pip import` or `requirements.txt`
- Use only the following approved libraries:
  - `requests`
  - `openai`
  - `psycopg`
  - `boto3`
  - `pymilvus`
  - `redis`

### Secrets Management

When needing a secret:

1. Request addition to `.env` file
2. Add metadata comment to `__main__.py`: `#--param <SECRET> "$<SECRET>"`
3. Retrieve in main function (not `__main__.py`):

```python
<SECRET> = args.get("<SECRET>", os.getenv("<SECRET>"))
```

## Service Integrations

### Redis Configuration

When you need to use Redis, do always 3 things:

1. Add to `__main__.py`:

```python
#--param REDIS_URL $REDIS_URL
#--param REDIS_PREFIX $REDIS_PREFIX
```

2. Access code for `<action>.<action>(args)`:

```python
rd = redis.from_url(args.get("REDIS_URL"), os.getenv("REDIS_URL"))
prefix = args.get("REDIS_PREFIX"), os.getenv("REDIS_PREFIX"))
# Always use prefix for all Redis Keys
```

3. Ensure there is `ENABLE_REDIS` in the `tests/.env` file.

### PostgreSQL Configuration

When you need to use Postgres, do always 2 things:

1. add to `__main__.py`:

```python
#--param POSTGRES_URL "$POSTGRES_URL"
```

2. use the code for `<action>.<action>(args)`:

```python
dburl = args.get("POSTGRES_URL", os.getenv("POSTGRES_URL"))
```

3. Ensure there is `ENABLE_REDIS` in the `tests/.env` file.

### S3 Configuration

When you need to use S3, do always 3 things:

1. Add to `__main__.py`:

```python
#--param S3_HOST $S3_HOST
#--param S3_PORT $S3_PORT
#--param S3_ACCESS_KEY $S3_ACCESS_KEY
#--param S3_SECRET_KEY $S3_SECRET_KEY
#--param S3_BUCKET_DATA $S3_BUCKET_DATA
```

2. Access code for `<action>.<action>(args)`:

```python
host = args.get("S3_HOST", os.getenv("S3_HOST"))
port = args.get("S3_PORT", os.getenv("S3_PORT"))
url = f"http://{host}:{port}"
key = args.get("S3_ACCESS_KEY", os.getenv("S3_ACCESS_KEY"))
sec = args.get("S3_SECRET_KEY", os.getenv("S3_SECRET_KEY"))
store_s3 = boto3.client('s3', region_name='us-east-1', endpoint_url=url, aws_access_key_id=key, aws_secret_access_key=sec)
store_bucket = args.get("S3_BUCKET_DATA", os.getenv("S3_BUCKET_DATA"))
```

3. Ensure there is `ENABLE_MINIO` in the `tests/.env` file.

### Milvus Configuration

When you need to use Milvus, do always 3 things:

1. Add to `__main__.py`:

```python
#--param MILVUS_HOST $MILVUS_HOST
#--param MILVUS_PORT $MILVUS_PORT
#--param MILVUS_DB_NAME $MILVUS_DB_NAME
#--param MILVUS_TOKEN $MILVUS_TOKEN
```

2. Access code for `<action>.<action>(args)`:

```python
uri = f"http://{args.get("MILVUS_HOST", os.getenv("MILVUS_HOST"))}"
token = args.get("MILVUS_TOKEN", os.getenv("MILVUS_TOKEN"))
db_name = args.get("MILVUS_DB_NAME", os.getenv("MILVUS_DB_NAME"))
client = MilvusClient(uri=uri, token=token, db_name=db_name)
```

3. Ensure there is `ENABLE_MILVUS` in the `tests/.env` file.

## Key Requirements Summary

- Serverless, stateless, independent functions
- Python-only backend development
- JSON input/output objects only
- Proper annotation comments in `__main__.py`
- Environment-based configuration management
- Support for Redis, PostgreSQL, S3, and Milvus

# Web Actions Development Guide

The following rules apply to write backend REST calls (aka web actions) for the frontend.

## Overview

Web actions are serverless functions that can be invoked via HTTP REST interface without requiring authentication credentials. They enable you to build web-based applications with backend logic accessible anonymously.

## Web Action Basics

### URL Structure

Web actions are accessible to the frontend with this structure

```
/api/my/{PACKAGE}/{ACTION}.{EXTENSION}
```

Note that an {ACTION} has a name, but it can be also be accesset as {NAME}/{SUBPATH} allowing an internal routing.

The {SUBPATH} is then available in the `__ow_path` argument.

### Creating Web Actions

Enable web functionality using in the `__main__.py` the

```
#--param web true
```

## HTTP Request Context

Web actions automatically receive HTTP request details as parameters:

### Available Parameters

- `__ow_method`: HTTP method (GET, POST, PUT, etc.)
- `__ow_headers`: Request headers as key-value map
- `__ow_path`: Unmatched path after action extension
- `__ow_user`: Authenticated user namespace (if auth required)
- `__ow_body`: Request body (base64 for binary, string otherwise)
- `__ow_query`: Unparsed query string

## Content Types and Extensions

### Supported Extensions

- `.json` - JSON response
- `.html` - HTML response
- `.http` - HTTP response (default if no extension)
- `.svg` - SVG response
- `.text` - Plain text response

### Example URLs

```
/api/my/guest/demo/hello.json    # JSON response
/api/my/guest/demo/hello.html    # HTML response
/api/my/guest/demo/hello.http    # HTTP response
/api/my/guest/demo/hello         # Defaults to .http
```

## Request Processing

### Parameter Precedence (highest to lowest)

1. Body parameters
2. Query parameters
3. Action parameters
4. Package parameters

### Input Formats

- **JSON**: `application/json` (default)
- **Form Data**: `application/x-www-form-urlencoded`
- **Raw Data**: Any other content type

### HTTP Methods

Supported methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `HEAD`, `OPTIONS`

## Best Practices

### Authentication and Authorization

- Web actions bypass OpenWhisk authentication
- Implement your own auth logic (OAuth, JWT, etc.)
- Use `__ow_user` when authentication annotation is enabled

### Content Type Handling

- Specify the right extension for the URL
- Default is `application/json` for objects, `text/html` for strings
- Use base64 encoding for binary data
