"""
Python Questions
----------------

Building community, one answer at a time.
"""

from setuptools import find_packages, setup

setup(
    name='python-questions',
    version='0.1',
    # url='',
    license='BSD',
    author='Dan Crosta',
    author_email='dcrosta@late.am',
    description='Building community, one answer at a time',
    long_description=__doc__,
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    install_requires=[
        'Flask >= 0.8',
        'Flask-PyMongo',
        'Flask-Tweepy',
        'Flask-Script',
        'requests',
        'pytz',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'pyq = pythonquestions.scripts:manager.run',
        ],
    },
    # tests_require=[
    #     'nose',
    # ],
    # test_suite='nose.collector',
)

