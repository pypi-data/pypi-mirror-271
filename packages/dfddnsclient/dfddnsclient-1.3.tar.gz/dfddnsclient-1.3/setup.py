from setuptools import setup, find_packages

setup(
    name='dfddnsclient',
    version='1.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dfddnsclient = dfddnsclient.app:main',
        ],
    },
    install_requires=[
        'flask',
        'schedule',
        'requests'
    ],
    # Other metadata
    author='Dartfox.org',
    author_email='mail@dartfox.org',
    description='this is a pilot ddns client',
    url='https://github.com/dartfoxltd/dfddnsclient',
)
