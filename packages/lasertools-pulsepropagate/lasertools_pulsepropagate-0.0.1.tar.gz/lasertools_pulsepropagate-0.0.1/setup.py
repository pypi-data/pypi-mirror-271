from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="lasertools_pulsepropagate",
    version="0.0.1",
    description="A module to handle simple pulse propagation with dispersion and nlo",
    license="GPLv3",
    long_description=long_description,
    author="brittonm",
    author_email="68578865+brittonm@users.noreply.github.com",
    url="https://github.com/lasertools/lasertools_pulsepropagate",
    download_url = 'https://github.com/lasertools/lasertools_pulsepropagate/archive/refs/tags/v_0_0_1.tar.gz',
    packages=["lasertools_pulsepropagate"],
    install_requires=[
        "lasertools_pulse",
        "lasertools_pulsenlo",
        "lasertools_pulsedispersion",
    ],
)
