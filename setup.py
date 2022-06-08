import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="kub-api",
    version="0.0.1",
    author="Ryan Miller",
    author_email="midnryanmiller@gmail.com",
    description="A python wrapper for the KUB API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prairiesnpr/kub-api",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["aiohttp", "pyyaml"],
)
