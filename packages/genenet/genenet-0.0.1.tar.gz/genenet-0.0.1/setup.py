import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genenet",
    version="0.0.1",
    author="gaoyuan",
    author_email="18434753515@163.com",
    description="Constructing gene association networks using chromosomal conformational capture technology based on three-dimensional space (3D-GeneNet)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gaoyuanccc/3D-GeneNet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)