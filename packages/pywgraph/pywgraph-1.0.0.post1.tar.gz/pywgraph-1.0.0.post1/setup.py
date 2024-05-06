from setuptools import setup, find_packages #type: ignore

with open("README.md", "r",) as f: 
    long_description = f.read()

setup(
    name="pywgraph",
    version="1.0.0.post1",
    description="A python implementation of weighted directed graphs where weights can be elements of a mathematical group",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="josek98",
    author_email="josemmsscc98@gmail.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"]
    }
)
