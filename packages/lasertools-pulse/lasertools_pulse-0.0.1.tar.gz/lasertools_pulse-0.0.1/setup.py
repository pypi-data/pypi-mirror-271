from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_pulse",
    version="0.0.1",
    description="A module to represent a laser pulse",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_pulse",
    download_url = 'https://github.com/lasertools/lasertools_pulse/archive/refs/tags/v_0_0_1.tar.gz',
    packages=["lasertools_pulse"],
    install_requires=[
        "numpy",
        "lasertools_rffthelper==0.0.1",
    ],
  classifiers=[
    'Programming Language :: Python :: 3.9',
  ],
)
