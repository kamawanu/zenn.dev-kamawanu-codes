python3 -mvenv .venv
. .venv/bin/activate
python3 -mpip install --upgrade pip
python3 -mpip install gunicorn mercurial
gunicorn --reload hgweb:application