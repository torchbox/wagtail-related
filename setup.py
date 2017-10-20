#!/usr/bin/env python

from wagtailautotagging import __version__

from setuptools import setup, find_packages

gc_language_extras = [
    'google-cloud-language>=0.29.0,<0.30',
    'beautifulsoup4>=4.5.1',
    'html5lib>=0.999,<1',
]

elasticsearch5_extras = [
    'elasticsearch>=5,<6',
]

dandelion_extras = [
    'beautifulsoup4>=4.5.1',
    'html5lib>=0.999,<1',
    'requests>=2.11.1,<3.0',
]


setup(
    name='wagtailautotagging',
    version=__version__,
    description='A module for Wagtail that provides auto tagging functionality for Wagtail.',
    author='Mikalai Radchuk',
    author_email='mikalai.radchuk@torchbox.com',
    url='https://github.com/torchbox/wagtailautotagging',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    long_description='See https://github.com/torchbox/wagtailautotagging for details',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'wagtail>=1.12',
    ],
    extras_require={
        'gc_language': gc_language_extras,
        'elasticsearch5': elasticsearch5_extras,
        'dandelion': dandelion_extras,
    },
    zip_safe=False,
)
