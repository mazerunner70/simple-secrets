import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplesecrets",
    version="0.0.1",
    author="mazerunner70",
    author_email="author@example.com",
    description="Manages credentials and other data you don't want to check in to a repo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mazerunner70/simplesecrets",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
