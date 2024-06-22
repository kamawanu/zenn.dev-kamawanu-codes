python3 -mvenv .venv
. .venv/bin/activate
python3 -mpip install --upgrade pip
python3 -mpip install gunicorn mercurial basic-auth-middleware
# https://github.com/unit9/basic-auth-middleware
gunicorn --reload hgweb:application