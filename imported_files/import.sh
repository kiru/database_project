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
python clip_genre.py
python clip_links.py

python person.py
#python biography.py
python directs.py
#python acts.py
#python writes.py
#python produces.py

#python biography.py
#python released.py
#python runs.py

#Imported tables into Oracle DB:
# - Language
# - Genre
# - Country

