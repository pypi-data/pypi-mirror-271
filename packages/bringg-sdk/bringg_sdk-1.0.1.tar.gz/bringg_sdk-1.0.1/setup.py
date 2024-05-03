from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="bringg_sdk",
    URL='https://github.com/elkhayyat/bringg_sdk',
    EMAIL='elkhayyat.me@gmail.com',
    AUTHOR='AHMED ELKHAYYAT',
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
