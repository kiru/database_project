#!/bin/bash
# Proper header for a Bash script.!

rm -f database.db
sqlite3 database.db < ../relations/create_all_tables.sql

python3 country.py
python3 language.py
python3 genre.py

python3 clip.py
python3 clip_rating.py
python3 clip_language.py
python3 clip_country.py
python3 clip_genre.py
python3 clip_links.py

python3 person.py
#python3 biography.py
python3 directs.py
python3 acts.py
#python3 writes.py
#python3 produces.py

#python3 biography.py
#python3 released.py
#python3 runs.py

#Imported tables into Oracle DB:
# - Language
# - Genre
# - Country

