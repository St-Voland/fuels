# fuels

# set up db
sudo apt-get install libpq-dev libodbc1 postgresql postgresql-contrib postgresql-12-postgis-3 postgis
python3 upload_okko.py

# Install
pipenv shell

python3 setup.py bdist_wheel && pip3 install dist/fuels-0.0.1-py3-none-any.whl

# Run
fuels run

usage: t.me/test20220226_bot

Actual bot name is in config, for the testing purposes, test20220226 has been created. The corresponding config example can be found in the repo.
