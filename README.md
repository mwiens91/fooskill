[![Python version](https://img.shields.io/badge/python-3.6%20|%203.7-blue.svg)](https://github.com/mwiens91/fooskill)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://github.com/prettier/prettier)

# fooskill

## WIP: work in progress

fooskill is a foosball leaderboard web app.

## Development server setup

### Part A: backend

For all following steps, make sure you're in the [`backend/`](backend/)
directory.

### Step 1: set up a Django-ready PostgreSQL database

First you need to setup op a PostgreSQL database. If you're running
Ubuntu, DigitalOcean's instructions are great:

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

### Step 2: let fooskill know about your database

Copy [`.env.example`](backend/.env.example) to `.env` and fill in the
`DATABASE_*` variables. All the other variables you can leave as-is,
although you probably want to set `DEBUG=True`.

### Step 3: set up your environment

Using a virtual environment (or otherwise), install requirements with
pip by running

```
pip3 install -r requirements.txt
```

### Step 4: make database migrations

To get your database tables set up, run

```
./manage migrate
```

### Step 5: collect static files

(This step is unnecessary if you set `DEBUG=True` in your `.env`.) Run

```
./manage collectstatic
```

### Step 6: create an admin account

Run

```
./manage createsuperuser
```

and follow the instructions that the command gives you.

### Step 7: run the server

Now you can run a local fooskill server with

```
./manage runserver
```

### Part B: frontend

coming in a bit
