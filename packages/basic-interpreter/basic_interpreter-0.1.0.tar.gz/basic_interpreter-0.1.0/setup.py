import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="basic_interpreter",
    version="0.1.0",
    author="riley",
    author_email="rileyjenner71@gmail.com",
    description="a BASIC interpreter for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rileeyyy/BASIC.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
