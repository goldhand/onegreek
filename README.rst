onegreek
==============================

A short description of the project.


LICENSE: BSD

Deployment
------------

Run these commands to deploy the project to Heroku:

.. code-block:: bash

    heroku create
    heroku addons:add heroku-postgresql:dev
    heroku addons:add pgbackups
    heroku addons:add sendgrid:starter
    heroku addons:add memcachier:dev
    heroku pg:promote HEROKU_POSTGRESQL_COLOR
    heroku config:add DJANGO_CONFIGURATION=Production
    heroku config:add DJANGO_SECRET_KEY=RANDOM_SECRET_KEY
    heroku config:add DJANGO_AWS_ACCESS_KEY_ID=YOUR_ID
    heroku config:add DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_KEY
    heroku config:add DJANGO_AWS_STORAGE_BUCKET_NAME=BUCKET
    git push heroku master
    heroku run python onegreek/manage.py syncdb --noinput --settings=config.settings
    heroku run python onegreek/manage.py migrate --settings=config.settings
    heroku run python onegreek/manage.py collectstatic --settings=config.settings
