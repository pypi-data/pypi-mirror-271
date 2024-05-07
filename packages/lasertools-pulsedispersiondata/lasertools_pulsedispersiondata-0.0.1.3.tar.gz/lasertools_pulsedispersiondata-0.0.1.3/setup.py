from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_pulsedispersiondata",
    version="0.0.1.3",
    description="A module to store data for laser pulse dispersion",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_pulsedispersiondata",
    download_url = 'https://github.com/lasertools/lasertools_pulsedispersiondata/archive/refs/tags/v_0_0_1_3.tar.gz',
    packages=["lasertools_pulsedispersiondata"],
    install_requires=[
        "numpy",
    ],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
    package_data={
        "lasertools_pulsedispersiondata": [
            "*/*.json"
        ],
    },
)
