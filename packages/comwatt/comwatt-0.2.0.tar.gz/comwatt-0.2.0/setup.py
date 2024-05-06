from setuptools import setup, find_packages

setup(
    version='0.2.0',
    name='comwatt',
    description='Python client for Comwatt',
    license='MIT',
    author='Christophe Godart',
    author_email='51CGO@armaghast.eu',
    install_requires=['selenium'],
    url='https://github.com/51CGO/comwatt',
    keywords=['Comwatt', 'client'],
    packages=['comwatt']
)
