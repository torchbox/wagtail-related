#!/usr/bin/env python
from setuptools import setup, find_packages

# Testing dependencies
testing_extras = [
    'flake8>=3.5.0',
    'isort>=4.3.4',
]

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
    name='wagtail-related',
    version='0.1.0',
    description='A module for Wagtail that finds related pages and tags for your pages.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Mikalai Radchuk',
    author_email='mikalai.radchuk@torchbox.com',
    url='https://github.com/torchbox/wagtail-related',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[
        'wagtail>=2.0',
    ],
    extras_require={
        'testing': testing_extras,
        'gc_language': gc_language_extras,
        'elasticsearch5': elasticsearch5_extras,
        'dandelion': dandelion_extras,
    },
    zip_safe=False,
)
