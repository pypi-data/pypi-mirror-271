from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'ESSL users management'
LONG_DESCRIPTION = 'Internal helper package for ESSL users management'
setup(
    name='espy_contact',
    version='0.8',
    packages=find_packages(),
    install_requires=[
        'bcrypt==4.1.2',
        'pytest==8.1.1',
        'pydantic==2.7.1',
        'sqlalchemy==2.0.29',
        'bson==0.5.10'
        ],
    author='Femi Adigun',
    author_email='femi.adigun@myeverlasting.net',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    keywords=['fastapi','ESSL','ReachAI']
)