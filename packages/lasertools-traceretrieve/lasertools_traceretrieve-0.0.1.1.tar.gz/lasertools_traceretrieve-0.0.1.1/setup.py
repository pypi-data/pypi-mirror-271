from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_traceretrieve",
    version="0.0.1.1",
    description="A module to reconstruct the phase of a pulse from a measurement",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_traceretrieve",
    download_url = 'https://github.com/lasertools/lasertools_traceretrieve/archive/refs/tags/v_0_0_1_1.tar.gz',
    packages=[
        "lasertools_traceretrieve",
        "lasertools_traceretrieve.algorithm",
        "lasertools_traceretrieve.resources",
    ],
    install_requires=[
        "numpy",
        "matplotlib",
        "numba",
        "lasertools_pulse",
        "lasertools_trace",
        "lasertools_traceprocess",
    ],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
