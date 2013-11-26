from datetime import datetime
from django.conf import settings
from django.utils.importlib import import_module
from .scheduler import seconds_to_date


def run_expiration():
    try:
        expirable_settings = settings.EXPIRABLES
    except AttributeError:
        print ''
        print '======================================================================'
        print 'You need to add EXPIRABLES to settings. See documentation for settings'
        print '======================================================================'
        print ''
        return
    for exp in expirable_settings:
        expirable_model = getattr(import_module('.'.join(exp['model'].split('.')[0:-1])), exp['model'].split('.')[-1])
        date_field = exp['date_field']
        query_filter = {'{}__lte'.format(date_field): seconds_to_date(exp['expires_after'])}

        if not 'action' in exp and exp.get('delete', True):
            delete_count = expirable_model.objects.filter(**query_filter).count()
            expirable_model.objects.filter(**query_filter).delete()
            print 'Deleted {delete_count} of {model}'.format(**{
                'delete_count': delete_count,
                'model': expirable_model.__name__,
            })
            continue

        if not 'action' in exp and exp.get('delete', True):
            #  Nothing to be done here as we have no custom action and we don't delete the model
            continue

        if 'action' in exp:
            action = getattr(import_module('.'.join(exp['action'].split('.')[0:-1])), exp['action'].split('.')[-1])
            expirables = expirable_model.objects.filter(**query_filter)
            should_delete = exp.get('delete', True)
            for expirable in expirables:
                action(expirable)
                if should_delete:
                    expirable.delete()
            if should_delete:
                delete_count = expirables.count()
                print 'Deleted {delete_count} of {model} after performing {action}'.format(**{
                    'delete_count': delete_count,
                    'model': expirable_model.__name__,
                    'action': action.__name__,
                })


def test_configuration():
    try:
        expirable_settings = settings.EXPIRABLES
    except AttributeError:
        print ''
        print '======================================================================'
        print 'You need to add EXPIRABLES to settings. See documentation for settings'
        print '======================================================================'
        print ''
        return
    errors = 0
    for exp in expirable_settings:
        try:
            expirable_model = getattr(import_module('.'.join(exp['model'].split('.')[0:-1])), exp['model'].split('.')[-1])
        except ImportError:
            errors += 1
            print 'invalid config for "{}"'.format(exp['model'])
            print 'Make sure you ty'
        except AttributeError:
            print 'Can not find model: "{}" (check for typos)'.format(exp['model'])
            errors += 1

        if 'date_field' not in exp:
            errors += 1
            print 'date_field missing from configuration for "{}"'.format(exp['model'])
    if errors == 0:
        print 'Configuration is valid'