#!/usr/bin/env python3
from model.entry import Entry

Entry(db_name="log.db").init_database()

# TODO: create vessel entry if not exists
# TODO: every hour create an entry
# TODO: 1) if day not exists create it - 2) if hour == 0, create new day
