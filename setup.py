from setuptools import setup

setup(
    name='time-tracker',
    author='Jakub Pieńkowski',
    description='Time tracking tool',
    packages=['time_tracker'],
    install_requires=[
        'tornado',
        'asyncpg'
    ],
    entry_points={
        'console_scripts': [
            'time-tracker=time_tracker:main'
        ]
    }
)
