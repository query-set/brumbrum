# Bruuuum!

## Prerequisites

In order to run the application locally you have to have `docker` along with `docker-compose` installed on your machine.

## Run application locally
Run it with the following:

```console
docker-compose up -d
```

and docker will take care about the rest.

## API usage

### Cars

#### `POST /cars`

Request:
`curl -X POST -H "Content-Type: application/json;charset=UTF-8" -d "{\"make\": \"honda\", \"model\": \"civic\"} 0.0.0.0:8000/cars`

Response:
```json
{
  "make" : "honda",
  "model" : "civic",
}
```

Status code: `201 CREATED`

*Note*: All names of _make_ or _model_ will be lowercased.

#### `GET /cars`

Request:
`curl -X GET -H "Content-Type: application/json;charset=UTF-8" 0.0.0.0:8000/cars`

Response:
```json
[
	{
		"id" : 1,
		"make" : "Volkswagen",
		"model" : "Golf",
		"avg_rating" : 5.0,
	},
	{
		"id" : 2,
		"make" : "Volkswagen",
		"model" : "Passat",
		"avg_rating" : 4.7,
	}
]
```

Status code: `200 OK`

#### `DELETE /cars/<id>`

Request:
`curl -X DELETE -H "Content-Type: application/json;charset=UTF-8" 0.0.0.0:8000/cars/2`

Response:
Blank response with status code `204 NO CONTENT`

### Rate

#### `POST /rate`

Request:
`curl -X POST -H "Content-Type: application/json;charset=UTF-8" -d "{\"car_id\": 1, \"rating\": 5} 0.0.0.0:8000/rate`

Response:
```json
{
  "car_id" : 1,
  "rating" : 5,
}
```

Status code: `201 CREATED`

### Popular

#### `GET /popular`

Request:
`curl -X GET -H "Content-Type: application/json;charset=UTF-8" 0.0.0.0:8000/popular`

Response:
```json
[
	{
		"id" : 1,
		"make" : "Volkswagen",
		"model" : "Golf",
		"rates_number" : 100,
	},
	{
		"id" : 2,
		"make" : "Volkswagen",
		"model" : "Passat",
		"rates_number" : 31,
	}
]
```

Status code: `200 OK`

## Ideas for further development

* There can be installed `drf_yasg` package for Swagger generation.
* Tests can be parametrized using e.g. `pytest.mark.parametrize` to keep code DRY.
* Tests for case when there is no internet and you cannot confirm the existence of given model.
* Separate services in `docker-compose` for both `dev` and `production`.
