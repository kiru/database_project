#!/bin/bash
# Proper header for a Bash script.!


python3 country.py
python3 language.py
python3 genre.py

python3 clip.py
python3 clip_rating.py
python3 clip_language.py
python3 clip_country.py
python3 clip_genre.py
python3 clip_links.py

#python3 person.py
#python3 biography.py
#python3 directs.py
#python3 writes.py
#python3 acts.py
#python3 produces.py

#python3 biography.py
#python3 released.py
#python3 runs.py

#Imported tables into Oracle DB:
# - Country
# - Language
# - Genre
# - Clip
# - Clip Rating
# - Clip Langauge
# - Clip Genre

#To import the csv files
#psql -h db.kiru.io -d db -U db -W -c "\copy clip(clip_id, clip_title, clip_year, clip_type) from 'clip.csv' with delimiter as ',' csv header
