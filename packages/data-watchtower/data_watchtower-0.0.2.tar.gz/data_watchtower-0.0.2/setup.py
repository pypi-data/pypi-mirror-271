from setuptools import setup, find_packages
from data_watchtower import __version__

setup(
    name='data_watchtower',
    version=__version__,
    packages=find_packages(exclude=['macros']),
    url='https://github.com/acracker/data_watchtower',
    license='MIT',
    author='acracker',
    author_email='acracker@163.com',
    description='Data quality inspection tool. Identify issues before your CTO detects them!',
    # tests_requires=[
    #     "pytest==8.2.0",
    #     "faker",
    #     "PyMySQL==1.1.0",
    #     "psycopg2==2.9.9",
    # ],
    install_requires=[
        "attrs==23.2.0",
        "peewee==3.17.0",
        "shortuuid==1.0.13",
        "tornado==6.4",
        "pandas==2.2.2",
        "polars==0.20.23",
        "connectorx==0.3.2",
    ],
)
