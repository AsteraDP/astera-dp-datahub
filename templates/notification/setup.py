from setuptools import find_packages, setup

setup(
    name="custom_action",
    version="1.0",
    packages=find_packages(),
    # if you don't already have DataHub Actions installed, add it under install_requires
    install_requires=["acryl-datahub-actions"]
)
