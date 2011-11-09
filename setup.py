import setuptools

import roan

README = ""

with open("README.rst") as f:
    README = f.read()


setuptools.setup(
    name='roan',
    version=roan.__version__,
    description='Django per-model cache purging',
    long_description=README,
    author='CobraTeam',
    author_email='francisco@franciscosouza.net',
    packages=['roan'],
    include_package_data=True,
    install_requires=['Django>=1.2', 'request==0.7.6'],
)
