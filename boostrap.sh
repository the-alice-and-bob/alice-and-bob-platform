#!/usr/bin/env zsh

echo "[*] Creating superuser"
python manage.py loaddata superuser.json

echo "[*] EzyCourse credentials fixtures"
python manage.py loaddata ezycourse.json

echo "[*] Populating academy tags fixtures"
python manage.py loaddata tags_fixtures.json

echo "[*] Populating academy courses fixtures"
python manage.py loaddata product_fixtures.json

echo "[*] Populating students fixtures"
python manage.py loaddata students_fixtures.json

echo "[*] Populating campaigns fixtures"
python manage.py loaddata maillist_fixtures.json

echo "[*] Populating users from EzyCourse (running script, it can take a while)"
#python manage.py loaddata students_fixtures.json
python manage.py populate_ezycourse_students

echo "[*] Populating user's selling courses"
python manage.py populate_ezycourse_sells
