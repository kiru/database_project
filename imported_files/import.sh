#!/bin/bash
# Proper header for a Bash script.!

rm -f database.db
sqlite3 database.db < ../relations/create_all_tables.sql

python country.py
python language.py
python genre.py

python clip.py
python clip_rating.py
python clip_language.py
python clip_country.py

python runs.py

python directs.py
python acts.py
