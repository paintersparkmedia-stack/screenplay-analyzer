from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="preston-screenplay-analyzer",
    version="0.1.0",
    author="Painter Spark Media",
    description="Preston - A screenwriting program for analyzing screenplays",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - using custom parser
    ],
    entry_points={
        "console_scripts": [
            "preston=preston.cli:main",
        ],
    },
)
