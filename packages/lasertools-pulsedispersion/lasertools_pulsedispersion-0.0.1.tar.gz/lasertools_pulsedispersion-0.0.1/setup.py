from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_pulsedispersion",
    version="0.0.1",
    description="A module to apply dispersion to a pulse",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_pulsedispersion",
    download_url = 'https://github.com/lasertools/lasertools_pulsedispersion/archive/refs/tags/v_0_0_1.tar.gz',
    packages=["lasertools_pulsedispersion", "lasertools_pulsedispersion.models"],
    install_requires=["numpy", "lasertools_pulsedispersiondata", "lasertools_pulse"],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
