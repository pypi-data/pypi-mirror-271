from setuptools import setup, find_packages

setup(
    name='django_bulk_updater',
    version='0.1',
    packages=find_packages(),
    description='A Django package for bulk updating with multithreading',
    author='Sushil2308',
    author_email='sushilprasad60649@gmail.com',
    url='https://github.com/Sushil2308/django-multi-bulk-updater.git',  # if applicable
    install_requires=[
        'Django>=3.0',
    ],
)