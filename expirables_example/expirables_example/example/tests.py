from datetime import datetime, timedelta
from django.conf import settings
from django_webtest import WebTest
from .expirables_example.expirables_example.example.models import BaseExpirable, BaseExpirableTwo, BaseExpirableThree
from .management.commands.expire_expirables import run_expiration
from .scheduler import schedule


class ExpirableTest(WebTest):
    def setUp(self):
        settings.EXPIRABLES = [
        {
            'model': 'squiggles.expirables.models.BaseExpirable',
            'date_field': 'created',
            'expires_after': schedule(days=1),
        },
        {
            'model': 'squiggles.expirables.models.BaseExpirableTwo',
            'date_field': 'created',
            'action': 'squiggles.expirables.models.custom_expiration_action',
            'delete': False,
            'expires_after': schedule(seconds=10),
        },
        {
            'model': 'squiggles.expirables.models.BaseExpirableThree',
            'date_field': 'created',
            'action': 'squiggles.expirables.models.custom_expiration_action',
            'delete': True,
            'expires_after': schedule(minutes=10),
        },
    ]

    def test_expirable(self):
        expirable_expire = BaseExpirable.objects.create(created=datetime.now() - timedelta(days=1))
        BaseExpirable.objects.create(created=datetime.now())
        expirable_dont_expire = BaseExpirable.objects.create(created=datetime.now())
        run_expiration()
        self.assertTrue(BaseExpirable.objects.filter(pk=expirable_dont_expire.pk).exists())
        self.assertFalse(BaseExpirable.objects.filter(pk=expirable_expire.pk).exists())

    def test_expirable_with_custom_action_no_delete(self):
        expirable_expire = BaseExpirableTwo.objects.create()
        expirable_dont_expire = BaseExpirableTwo.objects.create(created=datetime.now() + timedelta(days=1))
        run_expiration()
        self.assertTrue(BaseExpirableTwo.objects.filter(pk=expirable_dont_expire.pk).exists())
        self.assertTrue(BaseExpirableTwo.objects.filter(pk=expirable_expire.pk).exists())

    def test_expirable_with_custom_action_and_delete(self):
        expirable_expire = BaseExpirableThree.objects.create()
        expirable_dont_expire = BaseExpirableThree.objects.create(created=datetime.now() + timedelta(days=1))
        run_expiration()
        self.assertTrue(BaseExpirableThree.objects.filter(pk=expirable_dont_expire.pk).exists())
        self.assertFalse(BaseExpirableThree.objects.filter(pk=expirable_expire.pk).exists())
