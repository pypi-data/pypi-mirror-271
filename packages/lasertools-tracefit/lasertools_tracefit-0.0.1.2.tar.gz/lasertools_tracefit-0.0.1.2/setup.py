from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_tracefit",
    version="0.0.1.2",
    description="A module to fit a measured trace",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_tracefit",
    download_url = 'https://github.com/lasertools/lasertools_tracefit/archive/refs/tags/v_0_0_1_2.tar.gz',
    packages=["lasertools_tracefit", "lasertools_tracefit.models", "lasertools_tracefit.resources"],
    install_requires=[
        "numpy",
        "matplotlib",
        "pygad",
        "nlopt",
        "lasertools_rffthelper",
        "lasertools_pulsedispersion",
        "lasertools_pulsenlo",
        "lasertools_pulsemodel",
        "lasertools_pulse",
        "lasertools_trace",
        "lasertools_traceprocess",
        "lasertools_rffthelper",
    ],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
