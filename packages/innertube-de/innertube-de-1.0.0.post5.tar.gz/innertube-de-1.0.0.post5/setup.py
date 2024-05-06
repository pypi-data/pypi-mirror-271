from setuptools import find_packages
from setuptools import setup
from pathlib import Path


here = Path(__file__).parent
long_description = (here / "README.md").read_text()


setup(
    name="innertube-de",
    version="1.0.0-5",
    description="InnerTube Data Extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="g3nsy",
    author_email="g3nsydev@gmail.com",
    python_requires=">=3.6.0",
    url="https://github.com/g3nsy/innertube-de",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    install_requires=[],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
