from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding='utf-16') as f:
    required = f.read().splitlines()

setup(
    name="apollo-ai",
    version="0.0.43",
    description="Framework to process 3 channels in one: Video, Audio & Text",
    package_dir={"": "apollo"},
    packages=find_packages(where="apollo"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VerbaNexAI/APOLLO.AI",
    author="VerbaNex, Riddle",
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    extras_require={
        "dev": ["pytest>=7.4.3", "twine>=4.0.2"]
    },
    python_requires=">=3.10"
)
