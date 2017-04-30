# Captain's Log

A self-contained, automated store for all logbook entries on board a yacht.

This is in active development and is not ready for use yet.

## Setup

### Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

### Database Migrations

Create and run all database migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### First Time Use

Head to <http://127.0.0.1:8000/api/vessels> and make sure you at the very least create a vessel.

### Run

For the development server, run:

```bash
python manage.py runserver
```
