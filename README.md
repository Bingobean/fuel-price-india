# Fuel Price India

This API is created using python.

## Installation

Clone the repo and run,

```bash
python3 -m flask run --port=5000
```
This will launch the API server in port 5000

## Endpoints

- /states

This will return all the states that can be used to obtain data.

- /states/state

Here you have to pass in a state as parameter and it will return all the available cities within said state

- /price/city/fuelType

Here you pass in the city that you want to get data for and which fuel type you need.

fuelType = Petrol, Diesel

You can pass in only one fuelType.
