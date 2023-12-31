# Fuel Price India

It returns the petrol and diesel price of the particular city on that date.

This API is created using python.

## Installation (to run locally):

Clone the repo and run,

```
python -m flask run --port=5000
```
This will launch the API server in port 5000

Your Flask application is now available at `http://localhost:5000.`

## Endpoints:

Deployment Base URL - `https://fuelinr.vercel.app/`

- Method: GET - `/states`

This will return all the Indian states and cities that can be used to obtain data.

- Method: GET - `/state/<state>`

Here you have to pass in a state as parameter and it will return all the available cities within said state.

- Method: GET - `/cities`

This will return with all the cities irrespective of state that are available and the total number of cities.

- Method: GET - `/price/city/<fuelType>`

Here you pass in the city that you want to get data for and which fuel type you need.

fuelType = Petrol, Diesel

You can pass in only one fuelType.

## Examples:

1. GET - https://fuelinr.vercel.app/price/barmer/petrol

```
{
  "PETROL": {
    "city": "barmer",
    "currency": "INR",
    "date": "31/12/2023",
    "price": "110.26"
  }
}
```

2. GET - https://fuelinr.vercel.app/price/kanniyakumari/diesel

```
{
  "DIESEL": {
    "city": "kanniyakumari",
    "currency": "INR",
    "date": "31/12/2023",
    "price": "95.05"
  }
}
```

---

This is powered by Flask + Vercel with Serverless Functions.

---
