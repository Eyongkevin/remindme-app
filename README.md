# RemindMeApp

<img src="docs/home_full.png" width=500>

This is an app developed with Kivy that acts as a reminder. You can set some events and the app will play a sound when it's time.

## Features

## Configuration Page

- Set time and days for the alarm to be triggered
- Set a label for the event.
- Validation is set to activate the `Add` button only when required fields are filled.

## Reminder List Page

- List all reminders. The following things are listed for a reminder
  - Label
  - Time
  - event status, if active or not
  - event status, if passed or pending.

## Stopwatch Page

<img src="docs/stopwatch.png" width=150>

This page contains a clock that runs base on your system's time zone, and a stopwatch for timing tasks.

## Future Features

The app is still very young and under development. Here are some features that I am working on

- Select between popup and/or different sounds for the alarm
- A reminder can be added with a break length. Just like the pomodoro technique, we should have a count-down prior to the alarm been triggered.
- The homepage can show a maximum of 2 events. The event that just got triggered, with it's count-down if applicable, and the up-coming event. Then a small button is provided that shows all passed events in a popup.
- A search form in the `Reminder List Page` to search events.
- Filters to filter by `passed`, `pending`, `active`, `inactive`
- Ways to edit events from the `Reminder List Page`: We could have buttons to delete, activate and inactivate from the list page, but for edit, once we press the edit button, it should take us to the configuration page with all information pre-filled, ready to be edited.

## How to Install
This process of installation was tested on a macbook pro 2015 and 2023 version.

**NB**
- At the time of writing this readme, Kivy doesn't build with Python 3.12+.
- I am using `psycopg version 3` for this project. But I think `psycopg2` should work fine.

### Setup the postgresql database
- Log in as postgres user: `psql -U postgres` and do the following;
```postgresql
-- Create a user for this project and give it create db privileges 
CREATE USER <username> WITH PASSWORD '<password>';
ALTER USER <username> WITH CREATEDB;

-- connect to that user 
\c postgres <username>

--- create the database
CREATE DATABASE <db-name>

-- connect to the newly created database with the created user

\c <db-name> <username>

-- Make sure you are in the root directory and run the command.
-- This will create the table in the database
\i docs/script.sql
```

### Set up you .env file
- Create a  `.env` file in the root directory and replace values in `<>` with your values;

```
db_host=localhost
db_name=<db-name>
db_user=<username>
db_password=<password>
db_port=5432

```

### Install dependencies
- Create an source a virtual environment with `Python v3.11`

```bash
python3.11 -m venv .venv --prompt remindme-app
source .venv/bin/activate

```
- In the root directory, run the following command to install all packages
```bash
pip install -r requirements.txt
```

## Start the program
- Run `make` in the root directory
```bash
make
```

## How to contribute

**RemindMeApp** is an [open source](https://opensource.com/resources/what-open-source) project. I am open to suggestions and willing to extend it to a different level. Anyone willing to contribute is highly welcomed.
To contribute, go ahead and:

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :blush:
