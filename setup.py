import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="expirables",
    version="0.1.0",
    author="Jonas Hagstedt",
    author_email="hagstedt@gmail.com",
    description=("Django expirable models"),
    license="BSD",
    keywords="django expirables expiration expires",
    url = "https://github.com/jonashagstedt/django-expirables",
    packages=['expirables', ],
    long_description=read('README.md'),
    install_requires=[
        "Django >= 1.4",
    ],
    classifiers=[
        "Development Status :: Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
