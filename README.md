django expirables
=======================

Set an expiration time for your django models.


## Description

Expire django models after a certain time.

You can expire models after a set number of ```days``` / ```hours``` / ```minutes``` (or even ```seconds```)


## Installation 

1.  pip install -e git://github.com/jonashagstedt/django-expirables.git#egg=expirables

2. Add ```'expirables',``` to installed apps.


        INSTALLED_APPS = (
            ...
            'expirables',
         )

3. See the configuration section for setup.

4. Configure a cron job or a celery task.

For a cron job you can simple set it to call ```python /path/to/manage.py expire_expirables```

For a celery task you need to have celery installed and setup to run celery beat.
Create a new task that calls ```run_expiration``` (and make sure you import ```from expirables.expiration import run_expiration ```)


## Configuration

Add ```EXPIRABLES``` to your settings file.

The minimum requirements for settings is ``` { 'model': '...', 'date_field': '...' }```
where the model is the model you want to expire, and the date_field is the field containing the date.


Example configuration:

        EXPIRABLES = [
            {
                'model': 'myproject.someapp.models.ExpirableModel',
                'date_field': 'created',
                'action': 'myproject.someapp.custom_actions.custom_expiration_action',
                'delete': True,
                'expires_after': schedule(seconds=10),
            }
        ]


The ```schedule``` can be set with days, hours, minutes and seconds.
For instance, to set a model to expire after 2 days and 30 minutes you would set it up as follows:

        EXPIRABLES = [
            {
                ...
                'expires_after': schedule(days=2, minutes=30),
            }
        ]


## Additional notes
