from setuptools import setup

setup(
    name='snapshotanalyzer-3000',
    version='0.1',
    packages=['shotty'],
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
    '''
)