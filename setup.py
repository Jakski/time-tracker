import re
from setuptools import setup


def get_latest_version(changelog):
    '''Retrieve latest version of package from changelog file.'''
    # Match strings like "## [1.2.3] - 2017-02-02"
    regex = r'^##\s*\[(\d+.\d+.\d+)\]\s*-\s*\d{4}-\d{2}-\d{2}$'
    with open(changelog, "r") as changelog:
        content = changelog.read()
    return re.search(regex, content, re.MULTILINE).group(1)


setup(
    name='time-tracker',
    url='https://github.com/Jakski/time-tracker',
    author='Jakub Pieńkowski',
    author_email='jakub@jakski.name',
    license='MIT',
    description='Time tracking tool',
    version=get_latest_version('CHANGELOG'),
    packages=['time_tracker'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: MIT License'
    ],
    install_requires=[
        'tornado',
        'asyncpg'
    ],
    extras_require={
        'test': [
            'flake8'
        ]
    },
    entry_points={
        'console_scripts': [
            'time-tracker=time_tracker:main'
        ]
    }
)
