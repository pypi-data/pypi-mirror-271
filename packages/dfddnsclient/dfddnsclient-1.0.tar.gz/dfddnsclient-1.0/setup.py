from setuptools import setup, find_packages

setup(
    name='dfddnsclient',
    version='1.0',
    packages=find_packages(),
    scripts=['app.py'],
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
