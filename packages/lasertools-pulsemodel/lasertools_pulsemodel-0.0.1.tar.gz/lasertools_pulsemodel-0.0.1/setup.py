from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_pulsemodel",
    version="0.0.1",
    description="A module for pulse models",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_pulsemodel",
    download_url = 'https://github.com/lasertools/lasertools_pulsemodel/archive/refs/tags/v_0_0_1.tar.gz',
    packages=[
        "lasertools_pulsemodel",
        "lasertools_pulsemodel.model_amplitude",
        "lasertools_pulsemodel.model_phase",
    ],
    install_requires=[
        "numpy",
        "lasertools_pulse",
        "lasertools_rffthelper",
    ],
  classifiers=[
    'Programming Language :: Python :: 3.9',
  ],
)
