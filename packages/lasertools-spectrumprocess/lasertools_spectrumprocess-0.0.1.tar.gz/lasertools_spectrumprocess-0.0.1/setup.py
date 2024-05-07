from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_spectrumprocess",
    version="0.0.1",
    description="A module to process spectra",
    license="GPLv3",
    long_description=long_description,
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_spectrumprocess",
    download_url = 'https://github.com/lasertools/lasertools_spectrumprocess/archive/refs/tags/v_0_0_1.tar.gz',
    packages=["lasertools_spectrumprocess", "lasertools_spectrumprocess.utilities"],
    install_requires=[
        "numpy",
        "scipy",
    ],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
