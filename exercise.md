# API

### `POST /cars`

Request body should contain car make and model name.
Based on this data, its existence should be checked [here][https://vpic.nhtsa.dot.gov/api/]
If the car doesn't exist - return an error.
If the car exists - it should be saved in the database.

`Content-Type: application/json;charset=UTF-8`
```json
{
  "make" : "Volkswagen",
  "model" : "Golf",
}
```

### `DELETE /cars/{ id }`

Should delete the car with the given id from database.
If the car doesn't exist in database - return an error.

### `POST /rate`

Add a rate for a car from 1 to 5.

`Content-Type: application/json;charset=UTF-8`
```json
{
  "car_id" : 1,
  "rating" : 5,
}
```

### `GET /cars`

Should fetch a list of all cars already present in application database with their current average rate.

`Content-Type: application/json;charset=UTF-8`
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

### `GET /popular`

Should return top cars already present in the database ranking based on a number of rates (not average rate values, it's important!).

`Content-Type: application/json;charset=UTF-8`
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


## Rules & hints

* Your goal is to implement REST API in Django, however, you're free to use any third-party libraries and database of your choice, but please share your reasoning behind choosing them.
* Remember to name endpoints and fields exactly as in examples - your admission will be at one point tested automatically!
* Please do not paginate /popular and /cars responses.
* Make sure your API is accessible over HTTP
* At least basic tests of endpoints and their functionality are obligatory. Their exact scope and form is left up to you.
* The application's code should be kept in a public repository so that we can read it, pull it and build it ourselves. Remember to include README file or at least basic notes on application requirements and setup - we should be able to easily and quickly get it running.
* Please dockerize your application and use docker-compose or a similar solution.
* Written application must be hosted and publicly available for us online - we recommend Heroku.
