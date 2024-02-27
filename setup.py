from setuptools import setup, find_packages

requires = [
    'Django==4.2',
    'psycopg[binary]==3.1.12',
    'gunicorn==21.2.0',
    'python-dotenv==1.0.1',
    'djangorestframework==3.14.0',
    'drf-spectacular==0.27.1',
]

setup(
    name='mvp_crm',
    version='0.0',
    packages=find_packages(),
    install_requires=requires
)
