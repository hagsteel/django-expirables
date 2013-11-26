from datetime import datetime
from django.db import models


class BaseExpirable(models.Model):
    created = models.DateField(default=datetime.now)
    modified = models.DateField(default=datetime.now)

    def save(self, **kwargs):
        self.modified = datetime.now()
        super(BaseExpirable, self).save(**kwargs)


class BaseExpirableCustomAction(models.Model):
    created = models.DateField(default=datetime.now)
    modified = models.DateField(default=datetime.now)

    def save(self, **kwargs):
        self.modified = datetime.now()
        super(BaseExpirableCustomAction, self).save(**kwargs)


def custom_expiration_action(expirable):
    print 'ran custom action'
