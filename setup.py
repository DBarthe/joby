from setuptools import setup

setup(
    name='joby',
    version='0.2.3',
    packages=['joby'],
    url='',
    license='MIT',
    author='barth',
    author_email='barthelemy.delemotte@gmail.com',
    description='',
    install_requires=[
        'cassandra-driver',
        'requests',
        'geopy',
        'geohash2'
    ]
)
