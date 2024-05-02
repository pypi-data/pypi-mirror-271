from setuptools import setup, find_packages

setup(
    name='satsure-core',
    version='0.0.1',
    description='satsure core package',
    author='Satsure',
    author_email='kmstpm@email.com',
    packages=find_packages(),
    install_requires=['requests', 'fiona', 'pandas', 'pystac', 'python-dotenv',
                      'sqlalchemy'],
)
