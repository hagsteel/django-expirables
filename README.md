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

The minimum requirements for settings is ``` { 'model': '...', 'date_field': '...' 'expires_after': schedule(...)}```
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

## Settings ```EXPIRABLES``` explained:

### ```model```

is the model you want to expire. Make sure you type the entire path ```app.library.models.Model```

### ```date_field```

is the field on the model that expirables will use to check if enoguh time has lapsed and to expire the model.
Example fields would be ```date_created```, or if you want to renew the model every time it's updated you can use a ```modified``` field (and make sure you update the value each time you save the model)

### ```action```

is an action that runs on the model before it's expired (unless ```delete``` is set to False).
the action should take only one parameter and that's an instance of the model.

example:

        class MyModel(models.Model):
            name = models.CharField(max_length=100)
            created_date = models.DateTime(default=datetime.now)

        ...

        def my_custom_action(instance_of_my_model):
            print '{} has expired'.format(instance_of_my_model.name)

### ```delete```

This is True by default, however if you don't want to delete the instance, but change a value on the
model after a period of time, this could be done by combining ```delete: False``` and ```action```

### ```expires_after```

is the number of seconds that must have lapsed before the model is expired.
A convenience method is added called ```schedule```. Schedule will take days, hours, minutes and / or seconds and
convert that to a total number of seconds.

You could set ```expires_after: 60``` to let the model expire after 1 minute (60 seconds).


## Additional notes
The expiration won't occur until ```run_expiration``` is executed.
If you set your models to expire after 5 hours, but you call ```run_expiration``` once a day, the instance will still
exist after it's set expiration time, until ```run_expiration``` is called.

If high precision is a requirement, a suggestion is to filter out models that should have expired in the query set.
This will ensure that the model isn't showing up anywhere in your project even if it's not yet removed.


