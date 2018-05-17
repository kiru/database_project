#!/bin/bash
# Proper header for a Bash script.!

psql -h db.kiru.io -d db -U db -W \
    -c "\copy clip(clip_id, clip_title, clip_year, clip_type) from 'clip.csv' with delimiter as ',' csv header

#Imported tables into Oracle DB:
# - Country
# - Language
# - Genre
# - Clip
# - Clip Rating
# - Clip Langauge
# - Clip Genre

