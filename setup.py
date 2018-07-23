from distutils.core import setup

setup(
    # Application name:
    name="call-center",

    # Version number (initial):
    version="0.1.0",

    # Application author details:
    author="Victor Antonino",
    author_email="voa@cin.ufpe.br",

    # Packages
    packages=["app"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="http://pypi.python.org/pypi/CallCenter_v010/",

    #
    # license="LICENSE.txt",
    description="Useful towel-related stuff.",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "mock",
    ],
)