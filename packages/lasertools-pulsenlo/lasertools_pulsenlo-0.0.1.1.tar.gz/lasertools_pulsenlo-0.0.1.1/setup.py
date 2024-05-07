from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_pulsenlo",
    version="0.0.1.1",
    description="A module to apply simplified nonlinear processes to a pulse",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_pulsenlo",
    download_url = 'https://github.com/lasertools/lasertools_pulsenlo/archive/refs/tags/v_0_0_1_1.tar.gz',
    packages=["lasertools_pulsenlo", "lasertools_pulsenlo.models"],
    install_requires=["numpy", "scipy", "lasertools_pulse", "lasertools_rffthelper"],
    classifiers=[
      'Programming Language :: Python :: 3.9',
    ],
)
