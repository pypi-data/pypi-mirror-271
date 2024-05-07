from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_trace",
    version="0.0.1.1",
    description="A module to represent a pulse measurement trace",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_trace",
    download_url = 'https://github.com/lasertools/lasertools_trace/archive/refs/tags/v_0_0_1_1.tar.gz',
    packages=["lasertools_trace", "lasertools_trace.models"],
    install_requires=[
        "numpy",
        "lasertools_rffthelper",
        "lasertools_pulsenlo",
        "lasertools_pulsedispersion",
        "lasertools_pulse"
    ],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
