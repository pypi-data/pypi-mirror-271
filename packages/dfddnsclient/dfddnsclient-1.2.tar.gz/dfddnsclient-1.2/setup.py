from setuptools import setup, find_packages

setup(
    name='dfddnsclient',
    version='1.2',
    packages=find_packages(),
    scripts=['dfddnsclient/app.py'],
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
