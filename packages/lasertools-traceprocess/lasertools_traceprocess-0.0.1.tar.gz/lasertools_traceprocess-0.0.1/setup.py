from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_traceprocess",
    version="0.0.1",
    description="A module to process a pulse measurement trace",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_traceprocess",
    download_url = 'https://github.com/lasertools/lasertools_traceprocess/archive/refs/tags/v_0_0_1.tar.gz',
    packages=["lasertools_traceprocess", "lasertools_traceprocess.utilities"],
    install_requires=[
        "numpy", "scipy",
    ],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
