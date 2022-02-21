# Technical test

#### Setup

- Install python 3.7 & pipenv
- `pipenv install` to install project's requirements

#### Run

- `pipenv shell` to enter virtual environment (loading the variables in .env)
- `flask run`

#### Explore DB

Database is running on SQLite, it can be browsed using "DB Browser for SQLite" for instance

#### Expected work

1. Connect to La Poste API (https://developer.laposte.fr/)
2. Create an endpoint that fetch the status of a given letter on the La Poste API, and update it in the database
3. Create an endpoint that fetch the status of all letters on the La Poste API, and update it in the database
4. Make previous endpoint respond instantly, and launch an asynchronous task that update all the status

There is no need to do a front interface, you can just share a Postman collection to test it.

#### Bonus

- Unit, integration, E2E tests
- Store the status history of each letter in a new table
- Impress us

#### Test Data

Here are tracking IDs that you can use:
- 6A21757464334
- 6A22658410765

The current La Poste API Sandbox environment is currently down (for an unknown amount of time).
For now, you can use the Production environment keys.
