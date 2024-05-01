from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'ath sample test'

# Setting up
setup(
    name="ath_sample_lib",
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)