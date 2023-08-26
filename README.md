# 📈📉 Treasury Automation challenge

Here is a small app which should do forecasting for balance movements for Treasury team.
The whole feature is a pretty big one, but we need a quick prototype to showcase it for Treasury team,
so they can decide if this app better than Excel spreadsheets they are using right now.

## 🗺️Context

When our customer asks for service, basically her request is to transfer money from one place to another.
We [rely on network](https://docs.thunes.com/money-transfer/v2/#getting-started) of Sending and Receiving Partners (SP and RP).
Each RP has a balance associated with it. Each day can be many movements to a balance from different SPs.

Having historical balance movements, one can forecast what will be balance movements next days.
And the next important step: having balance movements forecast for today and having balance snapshot amount,
one can calculate required wire transfer, to top up the balance.
This forecasting and wire calculation is a minimum valuable product for Treasury.

## 📋Requirements

1. Provide API endpoint to run forecasting and wire transfer for a given date and balance id

   ```
   POST /api/v1/forecasting/{balance_id}/{forecasting_date}
   ```

   The app shall do one day forecasting, for a given day.

   Here you need to pick a forecasting method you'd like to use. The easiest is seven-day average:
   having previous 7 datapoints d1, d2, ..., d7, the forecast for today is `mean([d1, ..., d2])`.
   You may use more complicated tools, as ETS (exponential smoothing) or Prophet.

   Explore `balance_movements` table, it has some data, after you apply alembic migrations.
   For wire calculation you need to take `available_balance` from `receiving_partner_balances` table and forecasted balance movements.
   Then wire amount is `max(0, forecasted balance movements - available_balance)`. If there is enough money on a balance, wire transfer amount is zero.

2. Provide API to retrieve forecasted amount and wire amount for a given date and balance id.

   They should be persisted in database, it's also historical data, so that one can review what was forecasts and wire amounts for past day.

3. Finish ForecastingVariance feature to show variance for a given balance and data range.
   This feature is partly done. There is a web page with two tabs: chart (done) and table (to do).
   API endpoint is preset but returns mock data, so that's for you to implement it.

   Table shall have columns: date, actual amount, forecasted amount, variance, MAPE.
   MAPE is a mean absolute percentage metric.
   Chart shall display two curves: forecasted traffic and actual traffic.
   The page has Scale selector: (Daily, Weekly or Monthly), but you can implement everything with assumption
   that only Daily is used and show only daily traffic (both forecasted and actual).
   - Chart is done.

In terms of priorities, Wire Amount calculation is nice to have feature.
So you may drop it, if you are out of time.

### 💎 Quality requirements

We expect at least basic tests for web app and some test cases for python code (both for api and db parts).
This project has some examples.

Please state any assumptions that you make, or ask questions in case of ambiguity/incompleteness of requirements.

## 💻Development

### Database setup

You may use postgres from docker:

```bash
docker-compose up db
```

Then you can connect to it:

```bash
docker exec -it tfa-db-1 psql -U postgres -d tfa
```

### 🐍Python environment

Use [pyenv](https://github.com/pyenv/pyenv#installation) for easy switch between different Python versions

Install python and dependencies:

```zsh
pyenv install 3.10  # install required python version
pyenv local 3.10  # creates a .python-version file in your current directory

python -V  # check you have python 3.10

python -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
```

Then you can set variables from `.env` and run fastapi app:

```bash
uvicorn app.main:app --host 0.0.0.0 --reload --port 8000
```

There is also `docker-compose.yml` which bakes images, run alembic migrations and runs fastapi app with reload option and database.
So it can be useful for your development

#### Tests

```bash
PYTHONPATH=. pytest tests
```

### 🔮Web

Frontend development is done in JavaScript using Vue library. To start development, install nodejs first on your system.

Install [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) and then use it to install `node`:

```zsh
nvm install 15.4
nvm use 15.4
```

#### Installing dependencies

```zsh
$ cd web
$ yarn install
...
```

#### Configuration

There is a minimal config file: `.env.local`. Use this example to create your own `.env` files in the `app` and `web` directories.

#### Serving the application

From the `web/` directory I can run:

```zsh
$ cd web
$ yarn serve
INFO  Starting development server...
```

#### Tests

```zsh
$ cd web
$ yarn jest
 PASS  __tests__/app.test.js
  App
    ✓ renders the correct markup (7ms)

Test Suites: 1 passed, 1 total
Tests:       1 passed, 1 total
Snapshots:   0 total
Time:        2.904s
Ran all test suites.
```

## Support

If you have any questions, don't hesitate to ask via email <yunus.zaitaev@thunes.com> 🤝

## Delivery and next step

Kindly fork this repository, but don't create PR. Instead, add me (@dadwin) and Pierre (@pierre-vigier) as collaborators.
We will have a Panel Interveiew meeting to discuss your solution. Kindly prepare a short 5-10min overview/demo of your solution. Thank you in advance!

Good luck!!!
