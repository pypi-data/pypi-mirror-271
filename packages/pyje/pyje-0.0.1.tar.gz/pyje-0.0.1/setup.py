import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyje",
    version="0.0.1",
    author="jameskim",
    author_email="kibum1991@naver.com",
    description="Journal Entry with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jamesKim7/pyje",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)